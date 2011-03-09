require 'rubygems'
require 'open-uri'
require 'cgi'
require 'json'

nofetch = (ARGV.shift == "-n")

MAX_JITTER = 1_000 / ((2 * Math::PI / 360) * 6370e3) # 1km jitter

def jitter
  mult = rand < 0.5 ? 1 : -1
  MAX_JITTER * mult * rand
end

def emit_points(grant)
  log_value = Math.log10(grant['value'])

  log_value -= 5.0 # cutoff of £10_000

  num_points = 0

  while log_value > 1
    log_value -= 1
    num_points += 1
  end

  if rand < (log_value / 1.0)
    num_points += 1
  end

  num_points.times do |i|
    lat = grant['latlng']['lat'].to_f + jitter
    lng = grant['latlng']['lng'].to_f + jitter
    puts "#{grant['id']}-#{i},#{lat},#{lng}"
  end

  $stderr.print '.'
end

grant_files = Dir['grants/??/*.json']

grant_files.each do |file|

  grant = JSON.load(open(file).read)

  if !grant['latlng'] and !nofetch
    params = {
      'sensor' => 'false',
      'region' => 'GB',
      'address' => grant['organisation']['name']
    }

    params = params.map { |k, v| "#{CGI.escape(k)}=#{CGI.escape(v)}" }

    geocoding = open("http://maps.googleapis.com/maps/api/geocode/json?#{params.join('&')}").read
    geocoding = JSON.load(geocoding)

    if geocoding['status'] == "OK"
      grant['latlng'] = geocoding['results'].first['geometry']['location']

      File.open(file, 'w') do |f|
        $stderr.puts "added latlng to #{grant['id']}"
        JSON.dump(grant, f)
      end
    else
      $stderr.puts "geocode for #{grant['id']} returned status '#{geocoding['status']}'"
    end
  end

  if grant['latlng']
    emit_points(grant)
  end

end
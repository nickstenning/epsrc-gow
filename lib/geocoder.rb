require 'json'
require 'cgi'
require 'open-uri'

module Geocoder
  def self.geocode(org)
    $stderr.puts "geocoding '#{org.name}'"

    params = {
      'sensor' => 'false',
      'region' => 'GB',
      'address' => org.name
    }

    params = params.map { |k, v| "#{CGI.escape(k)}=#{CGI.escape(v)}" }

    geocoding = open("http://maps.googleapis.com/maps/api/geocode/json?#{params.join('&')}").read
    geocoding = JSON.load(geocoding)

    if geocoding['status'] == "OK"
      org.latlng = geocoding['results'].first['geometry']['location']
      org.save
    else
      $stderr.puts "WARNING: geocode for '#{org.name}' returned status '#{geocoding['status']}'"
    end
  end
end
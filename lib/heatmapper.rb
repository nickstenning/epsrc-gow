MAX_JITTER = 1_000 / ((2 * Math::PI / 360) * 6370e3) # 1km jitter

def jitter
  mult = rand < 0.5 ? 1 : -1
  MAX_JITTER * mult * rand
end

module Heatmapper
  def self.emit_points(grant)
    log_value = Math.log10(grant.value)

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
      lat = grant.organisation.latlng['lat'].to_f + jitter
      lng = grant.organisation.latlng['lng'].to_f + jitter
      puts "#{grant.id}-#{i},#{lat},#{lng}"
    end
  end
end
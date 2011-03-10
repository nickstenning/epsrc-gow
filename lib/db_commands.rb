require 'model'

module Commands

  def self.create
    require 'schema'
    Schema.up
  end

  def self.drop
    require 'schema'
    Schema.down
  end

  def self.lookup(id)
    $stderr.puts "Looking up grant #{id}:"
    g = Grant.find(id)

    if g
      y g.attributes
    else
      $stderr.puts "ERROR: Couldn't find grant in database."
    end
  end

  def self.geocode
    require 'geocoder'
    Organisation.all.each do |org|
      Geocoder.geocode(org) unless org.latlng
    end
  end

  def self.heatmap
    require 'heatmapper'
    Grant.all.each do |g|
      Heatmapper.emit_points(g) if g.organisation.latlng
    end
  end


  def self.loadscrape
    require 'yaml'
    require 'scrape_loader'
    YAML.load_documents(STDIN.read) do |d|
      ScrapeLoader.load(d)
    end
  end

end
require 'rubygems'

require 'yaml'
require 'digest/sha1'
require 'fileutils'

require 'json'

if ARGV.length != 1
  puts "Usage: #{File.basename($0)} <dbdir>"
  puts
  puts "Extracts YAML data scrape on STDIN into sharded database of JSON files."
  exit 1
end

dbdir = ARGV.shift

YAML.load_documents(STDIN.read) do |d|
  id = Digest::SHA1.hexdigest(d['id'])

  dir = dbdir + '/' + id[0..1]
  FileUtils.mkdir_p(dir)

  fname = dir + '/' + id + '.json'

  File.open(fname, 'w') do |f|
    puts "processing #{d['id']} -> #{fname}"
    JSON.dump(d, f)
  end
end

require 'rubygems'

require 'yaml'
require 'digest/sha1'

require 'json'

if ARGV.length != 1
  puts "Usage: #{File.basename($0)} <grant identifier>"
  puts
  puts "Looks up data for grant in local database (grants/ directory)."
  exit 1
end

id = ARGV.shift
hash = Digest::SHA1.hexdigest(id)

$stderr.puts "Looking up grant #{id} --> #{hash}"

file = "grants/#{hash[0..1]}/#{hash}.json"

begin
  json = open(file).read
  grant = JSON.load(json)
  y grant
rescue Errno::ENOENT
  $stderr.puts "ERROR: Couldn't find grant in database."
end
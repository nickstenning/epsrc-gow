require 'rubygems'

require 'yaml'
require 'mechanize'
require 'hpricot'

if ARGV.length != 1
  puts "Usage: #{File.basename($0)} <grant id>"
  puts
  puts "Retrieves EPSRC GOW data for a specifed grant."
  exit 1
end

grant_id = ARGV.shift

a = Mechanize.new
page = a.get("http://gow.epsrc.ac.uk/ViewGrant.aspx?GrantRef=#{grant_id}")

h = Hpricot(page.body)

def get_fkey_ids(elem, type, name = nil)
  name = type unless name

  elem.search("a[@href^='View#{name}']").map do |e|
    e['href'].match(/#{type}Id=(\-?\d+)/)[1].to_i
  end
end

mapping = {
  "Title:" => {
    "title" => proc { |e| e.at('span strong').innerText },
  },

  "Principal Investigator:" => {
    "principal_investigator_id" => proc { |e| get_fkey_ids(e, "Person").first }
  },

  "Other Investigators:" => {
    "other_investigator_ids" => proc { |e| get_fkey_ids(e, "Person") }
  },

  "Researcher Co-investigators:" => {
    "co_investigator_ids" => proc { |e| get_fkey_ids(e, "Person") }
  },

  "Project Partners:" => {
    "project_partner_ids" => proc { |e| get_fkey_ids(e, "Organisation", "Partner") }
  }
}

grant = {}

h.search("tr").each do |row|
  key = row.search("td")[0].innerText
  val = row.search("td")[1..-1]

  if m = mapping[key]
    m.each { |k, v| grant[k] = v.call(val) }
  end
end

y grant
require 'rubygems'

require 'yaml'
require 'mechanize'
require 'hpricot'

if ARGV.length != 1
  puts "Usage: #{File.basename($0)} <organisation id>"
  puts
  puts "Retrieves EPSRC GOW data for a specifed partner organisation."
  exit 1
end

organisation_id = ARGV.shift.to_i

a = Mechanize.new
page = a.get("http://gow.epsrc.ac.uk/ViewPartner.aspx?OrganisationId=#{organisation_id}")

h = Hpricot(page.body)

partner = {}
partner['id']   = organisation_id
partner['name'] = h.at("#lblPartnerName").innerText

y partner
require 'rubygems'

require 'yaml'
require 'mechanize'
require 'hpricot'

if ARGV.length != 1
  puts "Usage: #{File.basename($0)} <year>"
  puts
  puts "Retrieves EPSRC GOW data for financial year: 1 Apr <year> to 31 Mar <year + 1>"
  exit 1
end

financial_year = ARGV.shift.to_i
$stderr.puts "Retrieving data for FY#{financial_year}-#{financial_year+1}"

a = Mechanize.new

page = a.get('http://gow.epsrc.ac.uk/SearchPastGrant.aspx')

f = page.forms.first

f["oUcStartDate$ddlDay"] = 1
f["oUcStartDate$ddlMonth"] = 4
f["oUcStartDate$ddlYear"] = financial_year

f["oUcEndDate$ddlDay"] = 31
f["oUcEndDate$ddlMonth"] = 3
f["oUcEndDate$ddlYear"] = financial_year + 1

results = f.submit

h = Hpricot(results.body)

grantsrows = h.search('table tr:not(.GridHeader)')

grantsrows.each do |row|
  grant = {}
  anchors = row.search('a')

  grant['id']    = anchors[0]['title']
  grant['title'] = anchors[0].innerText

  grant['pi']              = {}
  grant['pi']['id_string'] = anchors[1]['href'].scan(/PersonId=(\-?\d+)/)[0][0]
  grant['pi']['id']        = grant['pi']['id_string'].to_i
  grant['pi']['name']      = anchors[1].innerText

  grant['organisation']              = {}
  grant['organisation']['id_string'] = anchors[2]['href'].scan(/OrganisationId=(\-?\d+)/)[0][0]
  grant['organisation']['id']        = grant['organisation']['id_string'].to_i
  grant['organisation']['name']      = anchors[2].innerText

  grant['department']              = {}
  grant['department']['id_string'] = anchors[3]['href'].scan(/DepartmentId=(\-?\d+)/)[0][0]
  grant['department']['id']        = grant['department']['id_string'].to_i
  grant['department']['name']      = anchors[3].innerText

  grant['value_string'] = row.search('span')[0]['title']
  grant['value'] = grant['value_string'].gsub(/[£,]/, '').to_f

  y grant
end
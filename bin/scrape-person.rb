require 'rubygems'

require 'yaml'
require 'mechanize'
require 'hpricot'

if ARGV.length != 1
  puts "Usage: #{File.basename($0)} <person id>"
  puts
  puts "Retrieves EPSRC GOW data for a specifed person."
  exit 1
end

person_id = ARGV.shift.to_i

a = Mechanize.new
page = a.get("http://gow.epsrc.ac.uk/ViewPerson.aspx?PersonId=#{person_id}")

h = Hpricot(page.body)

person = {}

person['id']   = person_id
person['name'] = h.at("#lblName").innerText

person['email'] = ''
encoded_email = h.at("#txtLink")['value']
encoded_email.scan(/./).each_slice(3) { |s| person['email'] << s.join.to_i.chr }

y person
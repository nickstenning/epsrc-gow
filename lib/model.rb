require 'connection'

class Grant < ActiveRecord::Base
  belongs_to :principal_investigator, :class_name => "Person", :foreign_key => "principal_investigator_id"
  belongs_to :organisation
  belongs_to :department
end

class Person < ActiveRecord::Base
  has_many :grants
end

class Organisation < ActiveRecord::Base
  has_many :grants
  has_many :departments

  serialize :latlng, Hash
end

class Department < ActiveRecord::Base
  has_many :grants
  belongs_to :organisation
end
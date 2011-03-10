class Schema < ActiveRecord::Migration

  def self.up
    create_table :grants, :id => false do |t|
      t.string :id, :limit => 12, :primary => true
      t.string :title
      t.decimal :value

      t.references :principal_investigator
      t.references :organisation
      t.references :department
      t.timestamps
    end

    create_table :organisations do |t|
      t.string :name
      t.string :latlng
      t.timestamps
    end

    create_table :departments do |t|
      t.string :name

      t.references :organisation
      t.timestamps
    end

    create_table :people do |t|
      t.string :name
      t.timestamps
    end
  end

  def self.down
    drop_table :people
    drop_table :departments
    drop_table :organisations
    drop_table :grants
  end

end
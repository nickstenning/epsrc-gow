{ 
  "dataset": {
    "model_rev": 1,
    "name": "epsrc-gotw",
    "label": "EPSRC Grants on the Web", 
    "description": "<p>This dataset will eventually be a complete scrape of the <a href=\"http://www.epsrc.ac.uk/\">Engineering and Physical Sciences Research Council</a>'s <a href=\"http://gow.epsrc.ac.uk/\">Grants on the Web</a>, providing information on public money granted to scientists for work in fields ranging from mathematics to materials science, and from information technology to structural engineering.</p> <p>Currently, it contains EPSRC past grants data (i.e. grants that have completed) from 1985 through to 2010. At last count, this included nearly 36,000 grants, totalling over £6B of funding.</p> <p>The dataset includes not only basic information about grants and the institutions and departments to which they were granted, but also industrial sector and research area classifications, as well as information on co-investigators and related grants.</p> <p>Please also note that the license terms of this data are  unclear, and as such this dataset should not currently be considered \"open data\".</p>",
    "currency": "GBP",
    "entry_custom_html": "<h3>This grant elsewhere on the web:</h3><ul><li><a href=\"http://gow.epsrc.ac.uk/ViewGrant.aspx?GrantRef=${entry.grant_reference}\">${entry.grant_reference} on <abbr title=\"Engineering and Physical Sciences Research Council\">EPSRC</abbr> Grants on the Web</a></li><li><a href=\"http://www.google.co.uk/search?q=&quot;${entry.grant_reference}&quot;\">Search for ${entry.grant_reference} on Google</a></li></ul>"
  },
  "mapping": {
    "from": {
      "fields": [
        {"constant": "EPSRC", "name": "label", "datatype": "constant"}
      ],
      "type": "entity",
      "description": "Body awarding the grant",
      "label": "Spender"
    },
    "to": {
      "fields": [
        {
          "column": "recipient",
          "datatype": "string",
          "default_value": "Unknown",
          "name": "label"
        }
      ],
      "type": "entity",
      "description": "The recipient of the grant.",
      "label": "Recipient"
    },
    "grant_reference": {
      "default_value": "",
      "description": "",
      "column": "grant_reference",
      "label": "Grant reference",
      "datatype": "string",
      "type": "value"
    },
    "amount": {
      "default_value": "",
      "description": "",
      "column": "amount",
      "label": "",
      "datatype": "float",
      "type": "value"
    },
    "grant_title": {
      "default_value": "",
      "description": "",
      "column": "grant_title",
      "label": "Grant title",
      "datatype": "string",
      "type": "value"   
    },
    "time": {
      "default_value": "",
      "description": "",
      "column": "start_date",
      "label": "Start date",
      "datatype": "date",
      "type": "value"
    },
    "time_end": {
      "default_value": "",
      "description": "",
      "column": "end_date",
      "label": "End date",
      "datatype": "date",
      "type": "value"
    },
    "grant_scheme": {
      "fields": [
        {
          "column": "grant_scheme",
          "datatype": "string",
          "default_value": "Unknown",
          "constant": "",
          "name": "label"
        }
      ],
      "label": "Grant award scheme",
      "type": "classifier",
      "description": "The EPSRC scheme under which the grant was awarded.",
      "taxonomy": "epsrc-gotw.epsrc-internal.scheme"
    },
    "grant_abstract": {
      "default_value": "",
      "description": "",
      "column": "grant_abstract",
      "label": "Grant abstract",
      "datatype": "string",
      "type": "value"   
    },
    "grant_final_report_summary": {
      "default_value": "",
      "description": "",
      "column": "grant_final_report_summary",
      "label": "Grant final report summary",
      "datatype": "string",
      "type": "value"   
    },
    "department": {
      "fields": [
        {
          "column": "department",
          "datatype": "string",
          "default_value": "Unknown",
          "constant": "",
          "name": "label"
        }
      ],
      "label": "Recipient department",
      "type": "classifier",
      "description": "The department receiving the grant within the recipient institution.",
      "taxonomy": "epsrc-gotw.recipient.department"
    },
    "institution": {
      "fields": [
        {
          "column": "institution",
          "datatype": "string",
          "default_value": "Unknown",
          "constant": "",
          "name": "label"
        }
      ],
      "label": "Recipient institution",
      "type": "classifier",
      "description": "The higher education institution receiving the grant.",
      "taxonomy": "epsrc-gotw.recipient.institution"
    }
  },
  "views": [
    {
      "entity": "dataset",
      "label": "By institution",
      "name": "default",
      "dimension": "dataset",
      "breakdown": "institution",
      "filters": {"name": "epsrc-gotw"}           
    },
    {
      "entity": "classifier",
      "label": "By department",
      "name": "default",
      "dimension": "institution",
      "breakdown": "department",
      "filters": {"taxonomy": "epsrc-gotw.recipient.institution"}           
    },   
    {
      "entity": "classifier",
      "label": "By recipient",
      "name": "default",
      "dimension": "department",
      "breakdown": "to",
      "filters": {"taxonomy": "epsrc-gotw.recipient.department"}           
    }, 
    {
      "entity": "dataset",
      "label": "By award scheme",
      "name": "scheme",
      "dimension": "dataset",
      "breakdown": "grant_scheme",
      "filters": {"name": "epsrc-gotw"}           
    }
  ]                       
}

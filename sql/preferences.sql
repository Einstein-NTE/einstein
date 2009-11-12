--
-- Table structure for table preferences
--

DROP TABLE IF EXISTS preferences;
CREATE TABLE preferences (
  id int(10) unsigned NOT NULL auto_increment,
  Font_facename varchar(45) default NULL,
  Font_family integer default 0,
  Font_style integer default 0,
  Font_weight integer default 0,
  Font_size integer default 10,
  Font_color varchar(16) default 0,
  user varchar(64) default NULL,
  PRIMARY KEY(id)
) TYPE=MyISAM;

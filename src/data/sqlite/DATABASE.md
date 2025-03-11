# Chinook database

## Overview
The Chinook sample database contains 11 tables.

## Tables

### employees table
- Stores employee data
- Key is Employeeid
- Joins:
  - To customers table on customers.SupportRepid = employees.Employeeid
- Column names:
  - Employeeid
  - LastName
  - FirstName
  - Title
  - ReportsTo
  - BirthDate
  - HireDate
  - Address
  - HireDate
  - Address
  - City
  - State
  - Country
  - PostalCode
  - Phone
  - Email

### customers table
- Stores customer data
- Key is Customerid
- Joins:
  - To employees table on customers.SupportRepid = employees.Employeeid
  - To invoices table on customers.Customerid = invoices.Customerid
- Column names:
  - Customerid
  - FirstName
  - LastName
  - Company
  - Address
  - City
  - State
  - County
  - PostalCode
  - Phone
  - Fax
  - Email
  - SupportRepid

### invoices table
- Stores invoice data, specifically invoice header data
- Key is invoiceid
- Joins:
  - To customers table on customers.Customerid = invoices.Customerid
  - To invoice_items table on invoice_items.invoiceid = invoices.invoiceid
- Column names:
  - invoiceid
  - Customerid
  - InvoiceDate
  - BillingAddress
  - BillingCity
  - BillingState
  - BillingCountry
  - BillingPostalCode
  - Total

### invoice_items table
- Stores invoice data, specifically invoice line items data
- Key is invoiceitemid
- Joins:
  - To tracks table on tracks.Trackid = invoice_items.Trackid
  - To invoice_items table on invoice_items.invoiceid = invoices.invoiceid
- Column names:
  - invoiceitemid
  - invoiceid
  - Trackid
  - UnitPrice
  - Quantity

### tracks table
- Stores the data of songs. Each track belongs to one album.
- Key is Trackid
- Joins:
  - To tracks table on tracks.Trackid = invoice_items.Trackid
  - To albums table on tracks.Albumid = albums.Albumid
  - To playlist_track table on tracks.Playlistid = playlist_track.Playlistid
  - To media_types table on tracks.MediaTypeid = media_types.MediaTypeid
  - To genres table on tracks.Genreid = genres.Genreid
- Column names:
  - Trackid
  - Name
  - Albumid
  - MediaTypeid
  - Genreid
  - Composer
  - Milliseconds
  - Bytes
  - UnitPrice

### albums table
- Stores data about a list of tracks
- Each album belongs to one artist, but an artist may have multiple albums
- Key is Albumid
- Joins:
  - To tracks table on tracks.Albumid = albums.Albumid
  - To artists table on artists.Artistid = albums.Artistid
- Column names:
  - Albumid
  - Title
  - Artistid

### artists table
- Stores artist data
- It is a simple table that contains the id and name
- Key is Artistid
- Joins:
  - To albums table on artists.Artistid = albums.Artistid
- Column names:
  - Artistid
  - Name

### genres table
- Stores music types such as rock, jazz, metal, etc.
- Key is Genreid
- Joins:
  - To tracks table on tracks.Genreid = genres.Genreid
- Column names:
  - Genreid
  - Name

### media_types table
- Stores media types such as MPEG audio and AAC audio files
- Key is MediaTypeid
- Joins:
  - To tracks table on tracks.MediaTypeid = media_types.MediaTypeid
- Column names:
  - MediaTypeid
  - Name

### playlist_track table
- playlists table stores data about playlists
- Each playlist contains a list of tracks
- Each track may belong to multiple playlists
- The relationship between the playlists and tracks tables is many-to-many. The playlist_track table is used to reflect this relationship.
- 2 keys are Playlistid and Trackid
- Joins:
  - To tracks table on tracks.Trackid = playlist_track.Trackid
- Column names:
  - Playlistid
  - Trackid

### playlists table
- playlists table stores data about playlists
- Each playlist contains a list of tracks
- Each track may belong to multiple playlists
- The relationship between the playlists and tracks tables is many-to-many. The playlist_track table is used to reflect this relationship.
- Key is Playlistid
- Joins:
  - To playlist_track table on playlists.Playlistid = playlist_track.Playlistid
- Column names:
  - Playlistid, INTEGER
  - Name, NVARCHAR(120)
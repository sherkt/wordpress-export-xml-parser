import csv
import xml.etree.ElementTree as ET

def parse_postmeta(input_file):
	tree = ET.parse(input_file)
	root = tree.getroot()
	items = root.findall('channel/item')

	ns = {'wp': 'http://wordpress.org/export/1.2/'}
	meta_id = 0

	columns = ['meta_id', 'post_id', 'meta_key', 'meta_value']
	data = [columns] # first row is the columns
	for item in items:
		post_id = item.find('wp:post_id', ns).text
		post_meta = item.findall('wp:postmeta', ns) or []
		# loop through post meta
		for meta in post_meta:
			meta_id += 1
			meta_key = meta.find('wp:meta_key', ns).text
			meta_value = meta.find('wp:meta_value', ns).text
			# add post meta for this post
			data.append(
				[meta_id, post_id, meta_key, meta_value]
			)

	return data

def parse_posts(input_file):
	tree = ET.parse(input_file)
	root = tree.getroot()
	items = root.findall('channel/item')

	ns = {
		'wp': 'http://wordpress.org/export/1.2/',
		'content': 'http://purl.org/rss/1.0/modules/content/',
		'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
	}

	columns = [
		'ID', 'post_author', 'post_date', 'post_date_gmt', 'post_content',
		'post_title', 'post_excerpt', 'post_status', 'comment_status',
		'ping_status', 'post_password', 'post_name', 'to_ping', 'pinged',
		'post_modified', 'post_modified_gmt', 'post_content_filtered',
		'post_parent', 'guid', 'menu_order', 'post_type', 'post_mime_type',
		'comment_count'
	]
	data = [columns] # first row is the columns
	for item in items:
		post_id = item.find('wp:post_id', ns).text
		post_author = 2 # you will need to modify this to match your author ID
		post_date = item.find('wp:post_date', ns).text
		post_date_gmt = item.find('wp:post_date_gmt', ns).text
		post_content = item.find('content:encoded', ns).text
		post_title = item.find('title', ns).text
		post_excerpt = item.find('excerpt:encoded', ns).text
		post_status = item.find('wp:status', ns).text
		comment_status = item.find('wp:comment_status', ns).text
		ping_status = item.find('wp:ping_status', ns).text
		post_password = item.find('wp:post_password', ns).text
		post_name = item.find('wp:post_name', ns).text
		to_ping = ''
		pinged = ''
		post_modified = item.find('wp:post_date', ns).text
		post_modified_gmt = item.find('wp:post_date_gmt', ns).text
		post_content_filtered = ''
		post_parent = item.find('wp:post_parent', ns).text
		guid = item.find('guid', ns).text
		menu_order = item.find('wp:menu_order', ns).text
		post_type = item.find('wp:post_type', ns).text
		post_mime_type = ''
		comment_count = len(item.findall('wp:comment', ns))
		data.append(
			[
				post_id, post_author, post_date, post_date_gmt,
				post_content, post_title, post_excerpt, post_status,
				comment_status, ping_status, post_password,
				post_name, to_ping, pinged, post_modified, post_modified_gmt,
				post_content_filtered, post_parent, guid, menu_order,
				post_type, post_mime_type, comment_count
			]
		)

	return data

def create_csv(data, filename):
	with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for row in data:
			writer.writerow(row)


input_file = 'wordpress_export_file.xml'

# post meta CSV
data = parse_postmeta(input_file)
create_csv(data, 'posts_meta.csv')

# posts CSV
data = parse_posts(input_file)
create_csv(data, 'posts.csv')

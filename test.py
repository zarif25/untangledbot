from scrapper import Provider

p = Provider("https://bdnews24.com/")
s = p.scrape_stories()[5]
s.scrape()
print(s.get_all())


# Published at 08:38 pm May 11th, 2021\n
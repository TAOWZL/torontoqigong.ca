#!/usr/bin/env python3
"""Builds the torontoqigong.ca static site into ../tq. Edit SITE and PAGES, rerun."""
import json, os, datetime

OUT = os.path.join(os.path.dirname(__file__), "..", "docs")
TODAY = datetime.date.today().isoformat()

SITE = {
    "name": "Toronto Qigong",
    "domain": "https://torontoqigong.ca",
    "operator": "Wuji Xuan Life Wellness Ltd",
    "street": "255 Broadview Ave, Ground Floor",
    "city": "Toronto", "region": "ON", "country": "CA",
    "postal": "",            # OPEN ITEM: paste postal code exactly as on the Google listing
    "phone": "416-595-5525", "phone_e164": "+14165955525",
    "email": "admin@wujixuan.org",  # OPEN ITEM: swap for an @torontoqigong.ca address if one is set up
    "noindex": True,         # flip to False at launch
    "sameAs": [],            # OPEN ITEM: Google listing URL, Instagram, Facebook, Eventbrite organiser page
}

NAV = [("index.html","Home"),("neigong-class.html","Saturday class"),("private-qigong-lessons.html","Private lessons"),
       ("online-qigong-class.html","Online"),("qigong-class-cost.html","Cost"),("what-is-neigong.html","What is neigong")]

def addr_line():
    p = f" {SITE['postal']}" if SITE["postal"] else ""
    return f"{SITE['street']}, {SITE['city']}, {SITE['region']}{p}"

def business_schema():
    a = {"@type":"PostalAddress","streetAddress":SITE["street"],"addressLocality":SITE["city"],
         "addressRegion":SITE["region"],"addressCountry":SITE["country"]}
    if SITE["postal"]: a["postalCode"] = SITE["postal"]
    s = {"@type":["LocalBusiness","EducationalOrganization"],"@id":SITE["domain"]+"/#school",
         "name":SITE["name"],"url":SITE["domain"]+"/","telephone":SITE["phone_e164"],"email":SITE["email"],
         "address":a,"areaServed":["Toronto","Riverdale","Leslieville","East York","Online"],
         "parentOrganization":{"@type":"Organization","name":SITE["operator"]},
         "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"10:00","closes":"11:00"}],
         "description":"Neigong and qigong classes in Toronto at 255 Broadview Ave. Saturday group class in person and online, private lessons through the week.",
         "makesOffer":[
           {"@type":"Offer","name":"Trial class","price":"20.00","priceCurrency":"CAD","description":"One Saturday neigong class. Plus HST."},
           {"@type":"Offer","name":"Monthly neigong subscription","price":"150.00","priceCurrency":"CAD",
            "priceSpecification":{"@type":"UnitPriceSpecification","price":"150.00","priceCurrency":"CAD","unitText":"MONTH"},
            "description":"Saturday class every week, the other group classes on the schedule, plus one 1-hour Reiki session or one 30-minute divination coaching session each month. Plus HST."}]}
    if SITE["sameAs"]: s["sameAs"] = SITE["sameAs"]
    return s

def faq_schema(faqs):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}

def faq_html(faqs):
    return "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in faqs)

def page(slug, title, desc, h1, lede, body, faqs=None, crumbs=True, extra_schema=None, cta_h='Book a trial class', cta_p=None):
    cta_p = cta_p or f"Text or call {SITE['phone']} to book the $20 trial."
    second_btn = '' if slug=='qigong-class-cost.html' else '<a class="btn ghost" href="/qigong-class-cost.html">See prices</a>'
    url = SITE["domain"] + "/" + ("" if slug=="index.html" else slug)
    graph = [business_schema()]
    if slug not in ("index.html","404.html"):
        graph.append({"@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Toronto Qigong","item":SITE["domain"]+"/"},
            {"@type":"ListItem","position":2,"name":h1,"item":url}]})
    if faqs: graph.append(faq_schema(faqs))
    if extra_schema: graph.extend(extra_schema)
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False, indent=1)
    cur = ' aria-current="page"'
    navhtml = "".join('<a href="/' + ("" if h=="index.html" else h) + '"' + (cur if h==slug else "") + '>' + t + '</a>' for h,t in NAV)
    robots = '<meta name="robots" content="noindex">' if SITE["noindex"] else ''
    crumb = f'<div class="crumbs"><a href="/">Toronto Qigong</a> / {h1}</div>' if (crumbs and slug!="index.html") else ""
    faqblock = f'<h2>Questions people ask</h2>\n{faq_html(faqs)}' if faqs else ""
    return f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{'' if slug=='404.html' else f'<link rel="canonical" href="{url}">'}
{robots}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<header class="site"><div class="wrap">
<a class="brand" href="/">Toronto Qigong<span>Neigong at 255 Broadview</span></a>
<nav class="main" aria-label="Main">{navhtml}</nav>
</div></header>
<section class="hero"><div class="wrap">
{crumb.replace('class="crumbs"','class="crumbs" style="color:#fdf2e3"').replace('<a href="/">','<a style="color:#FFEE72" href="/">')}
<h1>{h1}</h1>
<p class="lede">{lede}</p>
<a class="btn" href="sms:{SITE['phone_e164']}">Text {SITE['phone']} to book</a>
{second_btn}
</div></section>
<main><div class="wrap">
{body}
{faqblock}
<div class="cta">
<h2>{cta_h}</h2>
<p>{cta_p}</p>
<a class="btn" href="sms:{SITE['phone_e164']}">Text to book</a>
<a class="btn ghost" href="tel:{SITE['phone_e164']}">Call {SITE['phone']}</a>
</div>
</div></main>
<footer class="site"><div class="wrap">
<p><strong>{SITE['name']}</strong><br>{addr_line()}<br>
<a href="tel:{SITE['phone_e164']}">{SITE['phone']}</a> &middot; <a href="mailto:{SITE['email']}">{SITE['email']}</a><br>
Saturday class 10 to 11 am. Private lessons Tuesday to Sunday by appointment. Closed Mondays.</p>
<p>Toronto Qigong is the qigong and neigong school of {SITE['operator']}.</p>
</div></footer>
</body>
</html>
"""

from pages import PAGES  # content lives in pages.py

def main():
    os.makedirs(OUT, exist_ok=True)
    urls = []
    for p in PAGES:
        html = page(**p)
        with open(os.path.join(OUT, p["slug"]), "w", encoding="utf-8") as f: f.write(html)
        urls.append(SITE["domain"] + "/" + ("" if p["slug"]=="index.html" else p["slug"]))
    # 404 (real 404; host must serve it with status 404)
    nf = page(slug="404.html", title="Page not found | Toronto Qigong", desc="This page does not exist.",
              h1="That page is not here", lede="The link may be old. The class schedule, prices and booking are one click away.",
              body='<p>Try the <a href="/">home page</a>, the <a href="/neigong-class.html">Saturday class</a> or <a href="/qigong-class-cost.html">prices</a>.</p>', crumbs=False)
    nf = nf.replace('<meta name="robots" content="noindex">','').replace('<head>','<head>\n<meta name="robots" content="noindex">',1)
    open(os.path.join(OUT,"404.html"),"w",encoding="utf-8").write(nf)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls] + ["</urlset>"]
    open(os.path.join(OUT,"sitemap.xml"),"w").write("\n".join(sm)+"\n")
    open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE['domain']}/sitemap.xml\n")
    print("built", len(urls), "pages")

if __name__ == "__main__":
    main()

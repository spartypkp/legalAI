from tkinter import *
import markdown
import markdownify
import createAbe
import webbrowser
import os
DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    text = '''
# Understanding the Legality of Smoking Cannabis

## TLDR
Adults aged 21 and older can smoke cannabis under specific conditions in California, per Cal. Health and Safety Code § 11362.1. This article outlines the obligations and restrictions on cannabis possession, cultivation, processing, employment rights, consumption, and local jurisdictional regulations enshrined in California state law.

# Rights Granted To Users 

## Possessing, Processing, And Transporting Cannabis
### General Possession
Per California Health and Safety Code § 11362.1, adults (21+) can possess, process, transport, purchase, or donate to others (of similar age) up to 28.5 grams of non-concentrated cannabis and up to eight grams in its concentrated form.

### Growing Your Own Cannabis
Adults aged 21 and older are allowed to possess, plant, cultivate, harvest, dry, or process up to six living cannabis plants. They can concurrently possess the cannabis yield of these plants (Cal. HSC § 11362.1).

### Using Cannabis Accessories
Under Cal. HSC § 11362.1, Californian adults can possess, transport, purchase, obtain, use, manufacture, or give marijuana accessories to others who are 21 years or older.

## Consuming Cannabis 
### Cannabis Consumption
Users can smoke or ingest cannabis or cannabis products following state and local laws (Cal. HSC § 11362.1).

### Nonmedical Consumption
Adult individuals are allowed to consume nonmedical marijuana if they comply with California law, local standards, and regulations (Cal. CIV § 1550.5).

# Cannabis Usage Restrictions

## Restrictions on Public Consumption
### Prohibited Public Spaces
Smoking or ingestion of cannabis in public places prohibited areas for tobacco smoking is not allowed. This restriction extends to facilities, institutions, state or local government property, and within 1,000 feet of schools, daycare centers, or youth centers while children are present (Cal. HSC § 11362.3, § 11362.45).

### While Operating a Vehicle
Smoking or ingesting cannabis while driving a motor vehicle, boat, vessel, or aircraft is prohibited. Similarly, possession of open containers of cannabis while operating a vehicle is unlawful (Cal. HSC § 11362.3, Cal. HSC § 11362.45).

## Workplace Restrictions
### At Work
Employers have the right to maintain a drug and alcohol-free workplace. They can prohibit the use of cannabis by employees and prospective employees (Cal. HSC § 11362.45, Cal. GOV § 12954).

### On Job Sites
Smoking cannabis on the job or on the premises of a workplace during work hours is prohibited (Cal. HSC § 11362.785).

## Restrictions on Cultivations
### Personal Cultivations 
A personal cannabis indoor/homegrow facility must be a locked space not visible from the public place where cultivation takes place (Cal. HSC § 11362.2).

## Other Restrictions
### Cannabis Use in Healthcare Facilities
Smoking or vaping cannabis in healthcare facilities is prohibited (Cal. HSC § 1649.2).

### Underage Restrictions
Persons under the age of 21 are not allowed to purchase or possess cannabis or cannabis products (Cal. BPC § 26140).

# Exceptions to Restrictions
## Medical Usage
### Medical Exception
Medical cannabis use exceptions exist. A parent or guardian to a qualified patient can administer medicinal cannabis at a school site under certain conditions (Cal. HSC § 49414.1). Also, qualified patients or their caregivers can transport, process, administer, deliver, or give medicinal cannabis (Cal. HSC § 11362.765).

### During Probation or Bail
Users qualified for medical cannabis can request from the court for approval to use cannabis while on probation, bail, or parole (Cal. HSC § 11362.795).

# Local Jurisdictional Regulation
## Local Rules
Local jurisdictions can create and enforce ordinances to regulate the location, operation, or establishment of a medicinal cannabis cooperative or collective. Also, local jurisdictions can create rules to regulate businesses licensed under this division. The local jurisdiction can't prohibit the purchase and delivery of medicinal cannabis, but it can impose reasonable regulations relating to zoning requirements, security, public health and safety, licensing, and taxes (Cal. BPC § 26200, Cal. HSC § 11362.83, Cal. BPC § 26322).

#User Discrimination Protection
## Employment Discrimination
California law protects users from discrimination in hiring, termination, or any term or condition of employment based on that use (Cal. GOV § 12954).

## Cannabis Testing
### Quality Control
Users have the right to have cannabis products tested for quality control purposes by a licensed testing laboratory (Cal. BPC § 26104).

## Accommodating Medical Needs
### Medical Needs Exception 
If a physician recommends that the defined quantity does not meet the patient's needs, a patient may possess an amount of cannabis consistent with the patient's needs (Cal. HSC § 11362.77). Local counties may also have guidelines that allow patients or primary caregivers to exceed the state limits.


'''
    #markdown_to_html(text)
    #convert_markdown(text)
    open_html_in_browser("html_template.html")
    #open_html_in_browser("html_template.html")
    #html_to_markdown()



def markdown_to_html(text):
    section = '''{}'''.format(text)
    html_string = markdown.markdown(section, extensions=['md_in_html'])
    return html_string
    
    #open_html_in_browser("sample.html")

def html_to_markdown():
    with open("html_template.html", "r") as html_template:
        text = html_template.read()
    print(text)
    md = markdownify.markdownify(text)
    #print(md)

def open_html_in_browser(file_name="current.html"):
    new = 2 # open in a new tab, if possible

    # open a public URL, in this case, the webbrowser docs

    # open an HTML file on my own (Windows) computer
    url = "file://{}/{}".format(DIR, file_name)
    webbrowser.open(url,new=new)





def convert_markdown(md_text):
    split = md_text.split("\n")
    full_string = ""
    for line in split:
        if line == "":
            continue
        space_index = line.index(" ")
        start = line[0:space_index]
        if start == "#":
            result = "<h3>{}</h3>\n".format(line[space_index+1:])
        elif start == "##":
            result = "<strong>{}</strong>\n".format(line[space_index+1:])
        elif start == "###":
            result = "<p>  {}:</p>\n".format(line[space_index+1:])
        else:
            result = "<li>{}</li>\n".format(line)
        full_string += result
    print(full_string)

if __name__ == "__main__":
    main()
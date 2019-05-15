# SpaCy concept extraction
A simple spaCy-based concept extraction API, involving a dictionary of relevant concepts.

## Example usage

Request:

```
curl -X POST \
  http://35.231.89.123:5000 \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 4d1ebbfa-49ce-4e5e-a86c-4484e2741138' \
  -H 'cache-control: no-cache' \
  -d '[
	{
		"text":"This chapter introduces newly developed concepts about sustainable hazardous waste management and treatment and describes the key elements of sustainable hazardous waste management in the context of current broader issues (e.g., renewable energy and climate change). It also discusses fundamentals and basic components of sustainable hazardous waste and presents technical options for sustainable hazardous waste treatment and remediation. Microorganisms play an important role in wastewater treatment because of their immense potential for immobilization and bio-accumulative properties. Next, the chapter explains disposal of hazardous waste and reviews adjustments to meet global challenges. The choice of disposal should be based on evaluation of economics and potential pollution risks. Finally, the chapter identifies future trends and challenges for sustainable hazardous waste management/treatment, providing research recommendations to help achieve the broader goals of sustainability.",
		"@id": "/url/document"
		
	}
]'
```

Response:

```
{
    "text": "This chapter introduces newly developed concepts about sustainable hazardous waste management and treatment and describes the key elements of sustainable hazardous waste management in the context of current broader issues (e.g., renewable energy and climate change). It also discusses fundamentals and basic components of sustainable hazardous waste and presents technical options for sustainable hazardous waste treatment and remediation. Microorganisms play an important role in wastewater treatment because of their immense potential for immobilization and bio-accumulative properties. Next, the chapter explains disposal of hazardous waste and reviews adjustments to meet global challenges. The choice of disposal should be based on evaluation of economics and potential pollution risks. Finally, the chapter identifies future trends and challenges for sustainable hazardous waste management/treatment, providing research recommendations to help achieve the broader goals of sustainability.",
    "@id": "/url/document",
    "matches": [
        {
            "url": "http://eurovoc.europa.eu/6103",
            "label": "hazardous waste",
            "start": 8,
            "end": 10
        },
        {
            "url": "http://metadata.un.org/thesaurus#1006571",
            "label": "hazardous waste management",
            "start": 8,
            "end": 11
        },
        {
            "url": "http://eurovoc.europa.eu/1158",
            "label": "waste management",
            "start": 9,
            "end": 11
        },
        {
            "url": "http://eurovoc.europa.eu/6103",
            "label": "hazardous waste",
            "start": 20,
            "end": 22
        },
        {
            "url": "http://eurovoc.europa.eu/1158",
            "label": "waste management",
            "start": 21,
            "end": 23
        },
        {
            "url": "http://eurovoc.europa.eu/754",
            "label": "renewable energy",
            "start": 32,
            "end": 34
        },
        {
            "url": "http://metadata.un.org/thesaurus#1002035",
            "label": "energy",
            "start": 33,
            "end": 34
        },
        {
            "url": "http://metadata.un.org/thesaurus#1001030",
            "label": "climate change",
            "start": 35,
            "end": 37
        },
        {
            "url": "http://eurovoc.europa.eu/5482",
            "label": "climate change",
            "start": 35,
            "end": 37
        },
        {
            "url": "http://metadata.un.org/thesaurus#1006935",
            "label": "waste treatment",
            "start": 55,
            "end": 57
        },
        {
            "url": "http://eurovoc.europa.eu/1158",
            "label": "waste treatment",
            "start": 55,
            "end": 57
        },
        {
            "url": "http://eurovoc.europa.eu/5740",
            "label": "microorganism",
            "start": 59,
            "end": 60
        },
        {
            "url": "http://eurovoc.europa.eu/612",
            "label": "wastewater",
            "start": 65,
            "end": 66
        },
        {
            "url": "http://metadata.un.org/thesaurus#1005837",
            "label": "wastewater",
            "start": 65,
            "end": 66
        },
        {
            "url": "http://metadata.un.org/thesaurus#1001880",
            "label": "economics",
            "start": 103,
            "end": 104
        },
        {
            "url": "http://eurovoc.europa.eu/3933",
            "label": "economics",
            "start": 103,
            "end": 104
        },
        {
            "url": "http://metadata.un.org/thesaurus#030400",
            "label": "pollution",
            "start": 106,
            "end": 107
        },
        {
            "url": "http://metadata.un.org/thesaurus#1005003",
            "label": "pollution",
            "start": 106,
            "end": 107
        },
        {
            "url": "http://eurovoc.europa.eu/2524",
            "label": "pollution",
            "start": 106,
            "end": 107
        },
        {
            "url": "http://metadata.un.org/thesaurus#1005576",
            "label": "risk",
            "start": 107,
            "end": 108
        },
        {
            "url": "http://eurovoc.europa.eu/3728",
            "label": "risk",
            "start": 107,
            "end": 108
        },
        {
            "url": "http://eurovoc.europa.eu/8458",
            "label": "challenge",
            "start": 115,
            "end": 116
        },
        {
            "url": "http://metadata.un.org/thesaurus#1005498",
            "label": "research",
            "start": 123,
            "end": 124
        },
        {
            "url": "http://eurovoc.europa.eu/2914",
            "label": "research",
            "start": 123,
            "end": 124
        },
        {
            "url": "http://metadata.un.org/thesaurus#180703",
            "label": "recommendations",
            "start": 124,
            "end": 125
        },
        {
            "url": "http://metadata.un.org/thesaurus#1005390",
            "label": "recommendations",
            "start": 124,
            "end": 125
        },
        {
            "url": "http://eurovoc.europa.eu/2926",
            "label": "recommendation",
            "start": 124,
            "end": 125
        },
        ...
    ]
}
```

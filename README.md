# OpenReq - Improving Requirements Quality  

![EPL 2.0](https://img.shields.io/badge/License-EPL%202.0-blue.svg "EPL 2.0")

This component was created as a result of the OpenReq project funded by the European Union Horizon 2020 Research and 
Innovation programme under grant agreement No 732463.


## Technical Description

This stateless microservice checks requirements for quality issues. These quality issues include syntactic and semantic 
issues in the wording and phrasing of the requirements. The algorithms utilize simple NLP techniques to reach their
goals. This allows the microservice to be stateless and offer quick response times.

The algorithms implemented are from existing research, as well
as original research. The structure of the code allows interested parties to discover not only which work is from
existing work, but also how to find the original work. 

### Technologies Used

* Docker (-> https://www.docker.com/)

### How to Install

This microservice is Dockerized. With Docker installed on your machine, run the following commands to run the service:

1. `docker build --no-cache -t prs-improving-requirements-quality .`
    
    1. OR `docker build -t prs-improving-requirements-quality .` to cache
2. `docker run -p 9799:9799 prs-improving-requirements-quality`

### How to Use This Microservice

This microservice takes a number of textual requirements as input, and returns a number of noted issues with the
requirements quality. For detailed information on the endpoint(s), data format, and examples, see the Swagger file 
included in this repository, or the hosted version: <Include link to hosted Swagger once it is available>.

See "How to Install" above to run the service, followed by using a REST client to send requests.


### Notes for Developers

#### Updating requirements.txt
Run the following command to update the requirements.txt before pushing to GIT:
1) `venv/bin/pip freeze > requirements.txt`
2) Remove `en-core-web-sm==2.0.0` from requirements.txt

NOTE: If you run `pip freeze > requirements.txt` from a normal terminal, you will include all global packages, 
creating a bloated file. Please only use this command from a virtual environment where you are certain of the packages.

#### Running Tests

To run the tests:
1) Navigate to the root folder
2) Run `python tests/test_all.py`

#### Available Demos

**iFrame Functionality**: It is possible to query the functioning API in your web browser, with URL parameters, and it 
will act as a stand-alone page.
Instructions on Use:
1. Start the application locally using Docker and the above commands
2. Open the following your browser: 
`http://0.0.0.0:9799/index?requirementTitle=Requirement%20Title&requirementText=This%20is%20not%20a%20good%20requirement.`
3. Alter the URL Parameters as you want for different Titles and Text passed to the API

**CSV Input**: This is a demo package for a webpage that loads a CSV, and runs each requirement through the API.
1. Prepare a CSV file with a single column, where each row is a requirement
2. If you wish, separating sets of requirements with an empty line causes some visual formatting with the output

### Sources

##### Literature used in creating some of the algorithms (details can be found in the repository)

- Fleta MB. Technical Communication: Complex Nominals Used to Express new Concepts in Scientific English-Causes and 
Ambiguity in Meaning. ESPecialist. 1996;17(1):57-72.
- Landhaußer M, Korner SJ, Tichy WF, Keim J, Krisch J. DeNom: a tool to find problematic nominalizations using NLP. 
In Artificial Intelligence for Requirements Engineering (AIRE), 2015 IEEE Second International Workshop on 2015 Aug 24 
(pp. 1-8). IEEE.
- Yang H, Willis A, De Roeck A, Nuseibeh B. Automatic detection of nocuous coordination ambiguities in natural language 
requirements. InProceedings of the IEEE/ACM international conference on Automated software engineering 2010 Sep 20 
(pp. 53-62). ACM.
- Femmer H, Fernández DM, Juergens E, Klose M, Zimmer I, Zimmer J. Rapid requirements checks with requirements smells: 
Two case studies. InProceedings of the 1st International Workshop on Rapid Continuous Software Engineering 2014 Jun 3 
(pp. 10-19). ACM.
- Xu K, Liao SS, Li J, Song Y. Mining comparative opinions from customer reviews for Competitive Intelligence. Decision 
support systems. 2011 Mar 1;50(4):743-54.
- Gleich B, Creighton O, Kof L. Ambiguity detection: Towards a tool explaining ambiguity sources. InInternational 
Working Conference on Requirements Engineering: Foundation for Software Quality 2010 Jun 30 (pp. 218-232). Springer, 
Berlin, Heidelberg.
- Tjong SF, Berry DM. The design of SREE—a prototype potential ambiguity finder for requirements specifications and 
lessons learned. InInternational Working Conference on Requirements Engineering: Foundation for Software Quality 2013 
Apr 8 (pp. 80-95). Springer, Berlin, Heidelberg.


## How to contribute

See OpenReq project contribution 
[Contribution Guidelines](https://github.com/OpenReqEU/OpenReq/blob/master/CONTRIBUTING.md)


## License

Free use of this software is granted under the terms of the EPL version 2 (EPL2.0).

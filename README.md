# Gig Economy and Unemployment

This code repository is part of the submission of Assignment 2 of the Cluster and Cloud Computing course in Semester 1 2020 at the University of Melbourne.
The aim of this project is to use Platforms like Twitter and AURIN to extract data and process it so to present meaningful visualisations about the state of Australia and it's Cities.
In addition to the data processing and visualisation aspect of the project, this codebase shows how the team went about automating the creation and configuration of resources and applications on the Melbourne University NECTAR Research cloud

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

``` text
- Python
- Pip
- openstacksdk (python package)
```

The ansible playbook assumes the following:

```text
- The infrastricture resources will be created on the Melbourne Univeristy Research cloud using the openstack sdk
- The playbook initiator has access to the nectar cloud and has downloaded the necessary files (API key and openrc.sh file)
```

### Installing

TBC

## Deployment

To deploy the Infrastructure resources and configure them on the Nectar Research cloud follow the steps mentioned in the [USAGE.md](USAGE.md)

## Built With

- [Flash](https://flask.palletsprojects.com/en/1.1.x/) - Twitter Harvester Framework

## Authors

- **Sii Kim Lau** - *[student-id]* - [siil1](siil1@student.unimelb.edu.au)
- **Qing Feng Chye** - *[student-id]* - [qchye](qchye@student.unimelb.edu.au)
- **Yun Liu** - *[student-id]* - [yunliu1](yunliu1@student.unimelb.edu.au)
- **Rohan Jahagirdar** - *[student-id]* - [rjahagirdar](rjahagirdar@student.unimelb.edu.au)
- **Shorye Chopra** - *689913* - [shoryec](shoryec@student.unimelb.edu.au)

## Acknowledgments

- [Docker Swarm Reference Repository](https://github.com/atosatto/ansible-dockerswarm/tree/600b9913d8d219d1296994cb64ed7a46e1879808)

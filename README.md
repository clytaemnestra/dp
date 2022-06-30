## About 
My diploma thesis is focused on action rules - a specialized machine learning algorithm, which specifies which actions to take when certain confitions are met. The implementation package you can find in [this repository](https://github.com/lukassykora/actionrules) and more info about its implementation you can find in [this paper](http://ceur-ws.org/Vol-2644/paper36.pdf). 


The aim of my thesis was the following:
* to perform research on action rules & its existing implementations,
* to create a web interface, which allows users to filter action rules based on input parameters,
* and finally to evaluate the developed web interface by performing functional & usability tests with real users.

## Application
The main motivation for creation of such application is the fact that it's hard to filter the generated action rules. The idea is to create an interface, where non-technical users could enter attributes and get results with given attributes. Another benefit of using a web interface is data consistency - results are same for all users.

Application functionality is tested on [action rules](https://github.com/clytaemnestra/dp/blob/main/data/covid_action_rules_v11.ipynb) mined from the [Covid policy tracker dataset](https://github.com/OxCGRT/covid-policy-tracker). 

### Local Installation
Instructions for setup on Linux system are below. 
<details>

```sh
source venv/bin/activate

pip install requirements.txt

flask db migrate

flask db upgrade

flask run
```

</details>


### Screenshots
![obrazek](https://user-images.githubusercontent.com/38294198/176635694-b52332f0-4a56-4595-ab3d-3253a3040597.png)

![obrazek](https://user-images.githubusercontent.com/38294198/176635570-bec2160d-f595-4713-b462-01a84a2c77a5.png)

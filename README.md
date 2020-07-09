# Setup

#### Create local env file

Just run `make test_env`


#### Build containers

`docker-compose -f docker-compose-dev.yml build`

#### Before running project

- Create local env file and set up an email in it
- Build containers
- Run project

#### Run project

`docker-compose -f docker-compose-dev.yml up` or `make start_compose`


#### When project is running

- Apply db migrations `make migrations`
- Create superuser `make test_user`. After that you will be able to login into Admin
- Be happy

#### Create new app

`make app name=<app_name>`


#### All commands you can find in `Makefile`


# Django project description:
The project is a magazine-catalog of automobile brands and brands.

### Main roles:
   - User (the one who picks up his car)
   - Dealer (the one who puts cars up for sale)
	
## Scripts:
- The user can view all the cars, cars of a particular dealer or one car at a time
- User subscribes to the newsletter. When a new car is published, he / she receives an email
- The user places an order for the car of his choice.
- The dealer enters his login information. When registering, he receives an email with verification
- The dealer enters data about the new car. A new car is created with Pending status.
- The dealer changes the information about your car or its "status". His car has been updated.
- The dealer can choose the time of publication of the machine, and at the appointed time, the machine will be published
- Dealer can upload multiple pictures to his cars
- And other

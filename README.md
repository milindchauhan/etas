What are the legos?

- [x] start docker container from python script using docker-py
- [x] take the function file from the input and run it inside a running container
- [x] find out the total execution time of the container
- [ ] After a function finishes running, store the total execution time somewhere (in memory?)
- [ ] Get multiple network bound functions somehow (you might have to write them yourself)
- [ ] Create a static list of those functions which will act as a task queue. It will be randomized each run.
- [ ] implement etas
- [ ] record readings for multiple different values of alpha below 0.5.

Docker notes:
* You can't change the default command of an already created container. What you can do is start that container again without
having to re-create it. So if you get the same function again but with different inputs, you can probably rerun the container


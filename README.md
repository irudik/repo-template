# SEERE Repo Template

To use the repository template, either [fork](https://help.github.com/articles/fork-a-repo/) or [clone](https://help.github.com/articles/duplicating-a-repository/) into a new GitHub repository.

To clone:
1. Go to your GitHub home page, e.g. https://github.com/irudik
2. Click on the "+" sign to Create New Repository, called project-name
3. Open Git Bash
4. cd to the `git/` folder
5. Type `git clone --bare https://github.com/cornell-seere/repo-template.git`
6. Type `cd repo-template.git`
7. Type `git push --mirror https://github.com/irudik/project-name`
8. Remove the old repository, by typing `cd..`, then `rm -rf repo-template.git`

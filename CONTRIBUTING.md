# Introduction
Thank y'all for taking the time to contibute!

This an open source project and we love to receive contributions from our community — you! There are many ways to contribute, from writing tutorials or blog posts, improving the documentation, submitting bug reports and feature requests or writing code which can be incorporated into the project itself.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

### Important resources:
 - Overall information about TestIT: <https://testit.software/> 
 - TestIT URL for tests: <https://demo.testit.software/>

If you have any issues or you find someone's behavior unaccaptable, don't heistate to contact us at <support@testit.software>

# Set up your environment
In order to work with source code and run it you need:
 - python 3.4 or higher

Refer [README](README.rst) file for details

# Reporting issues and feature requests
## Security issues
If you find a security vulnerability, do NOT open an issue. Email <support@testit.software> instead.

In order to determine whether you are dealing with a security issue, ask yourself these two questions:

 - Can I access something that's not mine, or something I shouldn't have access to?
 - Can I disable something for other people?

If the answer to either of those two questions are "yes", then you're probably dealing with a security issue. Note that even if you answer "no" to both questions, you may still be dealing with a security issue, so if you're unsure, just email us at <support@testit.software>.

## Regular issues/suggestions
We kindly recommend you to follow issue template when filing a new one. Please, ensure that your statements are easy to understand and follow.

# Pull requests advices
Pull requests is the only acceptable contibution method.

## Make a pull request
 - You need a local fork of the Github repository.
 - Use a separate 'feature' branch for your changes. The branch should be followed by the feature/ prefix and have an undestantandable name describing the mail goal of the changes<br>
<i>Ex: features/Added_support_for_new_API.</i><br>
    `git checkout -b features/Added_support_for_new_API`
 - Fetch the actual version from origin/master and rebase your feature branch onto it before creating a pull request.<br>
    `git fetch -p`<br>
    `git rebase origin/master`
 - Push the branch to Github<br>
    `git push -u origin features/Added_support_for_new_API`
 - Visit Github, you should see a proposal to create a pull request
 <br><br>
 - If you need to add new commits to the pull request, you can simply commit the changed to the local branch and then push them to update the pull request<br>
    `git commit -m "Addressed pull request comments"`<br>
    `git push`

## Keeping your pull request up-to-date
We use rebase flow to keep your code up-to-date. If a maintainer asks you to "rebase" your PR, they're saying that a lot of code has changed, and that you need to update your branch so it's easier to merge.

`git fetch -p`<br>
`git rebase origin/master`<br>
`git push -f`

## Code review
The core team looks at pull requests on a regular basis in a weekly triage meeting. After feedback has been given we expect responses within two weeks. After two weeks we may close the pull request if it isn't showing any activity.

## Merging a PR (maintainers only)
A PR can only be merged into master by a maintainer if:

 - It is passing CI.
 - It has been approved by at least two maintainers. If it was a maintainer who opened the PR, only one extra approval is needed.
 - It has no requested changes.
 - It is up to date with current master.
 - Any maintainer is allowed to merge a PR if all of these conditions are met.

# Code style
Consider the people who will read your code, and make it look nice for them.
## Basic rules
 - We use spaces (not tabs). 4 spaces for an ident
 - Lines should not be longer than 120 characters per line. But try to keep it shorter (90 characters are reasonable compromise)
 - Add two empty lines between class declaration and a single empty line between me
 - Put imports on a separate line<br>
Correct:<br>
&nbsp;&nbsp;&nbsp;&nbsp;`import os`<br>
&nbsp;&nbsp;&nbsp;&nbsp;`import sys`<br>
Incorrect: <br>
&nbsp;&nbsp;&nbsp;&nbsp;`import sys, os`
 - But it is OK to use multiple imports from a component:<br>
&nbsp;&nbsp;&nbsp;&nbsp;`from subprocess import Popen, PIPE`
 - We follow general python code style standards: <https://www.python.org/dev/peps/pep-0008/>

## Line endings
We recommend to use LF line endings. This is how you can set them up for your git repo:<br>
`git config --global core.eol lf`<br>
`git config --global core.autocrlf input`<br>
`git rm -rf --cached .`<br>
`git reset --hard HEAD`


    
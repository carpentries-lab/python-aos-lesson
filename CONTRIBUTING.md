# Contributing

[Data Carpentry][dc-site] is an open source project
and we welcome contributions of all kinds
to the Python for Atmosphere and Ocean Science (PyAOS) materials:
new lessons,
fixes to the existing lessons,
bug reports,
and reviews of proposed changes are all welcome.

## Contributor Agreement

By contributing,
you agree that we may redistribute your work under [our license](LICENSE.md).
In exchange,
we will address your issues and/or assess your change proposal as promptly as we can,
and help you become a member of the PyAOS Data Carpentry community.
Everyone involved in Data Carpentry
agrees to abide by our [code of conduct](CONDUCT.md).

## How to Contribute

The easiest way to get started is to file an issue
to tell us about a spelling mistake,
some awkward wording,
or a factual error.
This is a good way to introduce yourself
and to meet some of our community members.

1.  If you do not have a [GitHub][github] account,
    you can send comments to the general Carpentries [email address][email].
    However,
    we will be able to respond more quickly if you use one of the other methods described below.

2.  If you have a [GitHub][github] account,
    or are willing to [create one][github-join],
    but do not know how to use Git,
    you can report problems or suggest improvements by [creating an issue][issues].
    This allows us to assign the item to someone
    and to respond to it in a threaded discussion.

3.  If you are comfortable with Git,
    and would like to add or change material,
    you can submit a pull request (PR).
    Instructions for doing this are [included below](#using-github).

## Structure of the respository

This respository contains all the code that generates the lesson website at
<https://carpentries-lab.github.io/python-aos-lesson/>.

In creating this repository,
we have used The Carpentries [lesson template][lesson-template].
The key files and directories are as follows:
- `index.md`: landing page for the website
- `setup.md`: software installation instructions
- `_episodes/`: directory containing the markdown file corresponding to each lesson/episode
- `_extras/`: directory containing the markdown file corresponding to each extras page at the website

When proposing changes to any of these markdown files, you may find the
[formatting instructions](https://carpentries.github.io/lesson-example/04-formatting/index.html)
at the lesson template site useful.

## Using GitHub

If you choose to contribute via GitHub,
you may want to look at
[How to Contribute to an Open Source Project on GitHub][how-contribute].
In brief:

1.  The published copy of the lesson is in the `gh-pages` branch of the repository
    (so that GitHub will regenerate it automatically).
    Please create all branches from that,
    and merge the [master repository][repo]'s `gh-pages` branch into your `gh-pages` branch
    before starting work.
    Please do *not* work directly in your `gh-pages` branch,
    since that will make it difficult for you to work on other contributions.

2.  We use [GitHub flow][github-flow] to manage changes:
    1.  Create a new branch in your desktop copy of this repository for each significant change.
    2.  Commit the change in that branch.
    3.  Push that branch to your fork of this repository on GitHub.
    4.  Submit a pull request from that branch to this repository.
    5.  If you receive feedback,
        make changes on your desktop and push to your branch on GitHub:
        the pull request will update automatically.


## Other Resources

General discussion of [Software Carpentry][swc-site] and [Data Carpentry][dc-site]
happens on the [discussion mailing list][discuss-list],
which everyone is welcome to join.
You can also [reach us by email][email].

[email]: https://carpentries.org/contact/
[dc-site]: http://datacarpentry.org/
[discuss-list]: http://lists.software-carpentry.org/listinfo/discuss
[github]: https://github.com
[github-flow]: https://github.com/dmgt/swc_github_flow/blob/master/for_novice_contributors.md
[github-join]: https://github.com/join
[how-contribute]: https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github
[issues]: https://github.com/carpentries-lab/python-aos-lesson/issues
[lesson-template]: https://carpentries.github.io/lesson-example
[swc-site]: https://software-carpentry.org/

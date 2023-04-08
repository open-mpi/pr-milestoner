# Pull Request Milestoner
A minor action which assigns milestones to pull requests based off of the
`MAJOR.MINOR` version of the base branch. If multiple milestones match that
form, the milestone with the closest due date is assigned. The action will only
apply a milestone if there currently isn't one already applied - this is to
prevent human-assigned milestones from getting overwritten.

*Uses [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html)*

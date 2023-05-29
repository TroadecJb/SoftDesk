from rest_framework.exceptions import NotFound
from api.models import Project, Contributor, Issue, Comment
from account.models import CustomUser


def project_exists(project_id):
    try:
        Project.objects.get(id=project_id)
        return True
    except Project.DoesNotExist:
        raise NotFound


def issue_exists(issue_id):
    try:
        Issue.objects.get(id=issue_id)
        return True
    except Issue.DoesNotExist:
        raise NotFound


def comment_exists(comment_id):
    try:
        Comment.objects.get(id=comment_id)
        return True
    except Comment.DoesNotExist:
        raise NotFound


def user_exists(user_id):
    try:
        CustomUser.objects.get(id=user_id)
        return True
    except CustomUser.DoesNotExist:
        raise NotFound


def contributor_exists(contributor_id):
    try:
        Contributor.objects.get(id=contributor_id)
        return True
    except Contributor.DoesNotExist:
        raise NotFound


def user_is_contributor(user_id, project_id):
    """
    Checks if the user and the project exists, then checks if the user is in the contributors' project.
    """
    if user_exists(user_id) and project_exists(project_id):
        for contributor in Contributor.objects.filter(project=project_id):
            if user_id == contributor.user.id:
                return True
            else:
                pass
    return False

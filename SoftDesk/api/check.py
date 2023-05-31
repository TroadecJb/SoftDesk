from rest_framework.exceptions import NotFound
from api.models import Project, Contributor, Issue, Comment
from account.models import CustomUser


def project_exists(project_id) -> bool or NotFound:
    """
    Return boolean 'True' if the project is in the db.
    Raise 'NotFound' exception if not.
    """
    try:
        Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise NotFound
    else:
        return True


def issue_exists(issue_id: int) -> bool or NotFound:
    """
    Return boolean 'True' if the issue is in the db.
    Raise 'NotFound' exception if not.
    """
    try:
        Issue.objects.get(id=issue_id)
    except Issue.DoesNotExist:
        raise NotFound
    else:
        return True


def comment_exists(comment_id) -> bool or NotFound:
    """
    Return boolean 'True' if the comment is in the db.
    Raise 'NotFound' exception if not.
    """
    try:
        Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise NotFound
    else:
        return True


def user_exists(user_id) -> bool or NotFound:
    """
    Return boolean 'True' if the user is in the db.
    Raise 'NotFound' exception if not.
    """
    try:
        CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        raise NotFound
    else:
        return True


def contributor_exists(contributor_id) -> bool or NotFound:
    """
    Return boolean 'True' if the contributor is in the db.
    Raise 'NotFound' exception if not.
    """
    try:
        Contributor.objects.get(id=contributor_id)
    except Contributor.DoesNotExist:
        raise NotFound
    else:
        return True


def user_is_contributor(user_id, project_id) -> bool:
    """
    Checks if the user and the project exists (raise 'NotFound' exception if either is not).
    Return boolean 'True' if the user is in the contributors' project list, else 'False'.
    """
    if user_exists(user_id) and project_exists(project_id):
        for contributor in Contributor.objects.filter(project=project_id):
            if user_id == contributor.user.id:
                return True
            else:
                pass
    return False

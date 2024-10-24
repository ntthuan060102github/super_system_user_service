from rest_framework.routers import SimpleRouter

from appbase.views.user.anonymous_user import AnonymousUserView

router = SimpleRouter(False)
router.register("user", AnonymousUserView, "user")
urls = router.urls
from django.contrib import admin
from account.models import Profile, Position
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

admin.site.register(Position)


class UserProfileInline(admin.StackedInline):
    model = Profile

    can_delete = False


class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]


# unregister old user admin
admin.site.unregister(User)

# register new user admin
admin.site.register(User, UserAdmin)

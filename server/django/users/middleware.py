from axes.handlers.proxy import AxesProxyHandler

from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import resolve


class CustomAdminAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 管理画面へのアクセスかつカスタム認証がまだなら認証ページへリダイレクト
        if request.path.startswith(
            "/admin/KOgEdTnMXbsDJa8jK347oaVqVzbshgIfhOWBjim9uEA5RfsEpl/"
        ) and not request.session.get("custom_admin_auth", False):
            return redirect("/custom-admin-auth/")
        response = self.get_response(request)
        return response


class CustomAxesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # resolve() を使用して現在のurls.pyのnameを取得
        resolved_path_name = resolve(request.path_info).url_name

        # urls.pyのnameを使用して特定のビューを識別
        if resolved_path_name in ["signup", "login", "change_username"]:
            # IPアドレスがブロックされているかチェック
            if AxesProxyHandler.is_locked(request):
                return HttpResponseForbidden("現在のIPアドレスからのアクセスは禁止されています。")

        response = self.get_response(request)
        return response

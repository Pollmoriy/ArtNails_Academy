from flask import Blueprint, redirect, url_for, flash

payments_bp = Blueprint("payments", __name__)

@payments_bp.route("/payment/success")
def payment_success():
    flash("Оплата прошла успешно 🎉 Спасибо за запись!", "success")
    return redirect(url_for("main.index"))

@payments_bp.route("/payment/cancel")
def payment_cancel():
    flash("Оплата не была завершена ❌ Попробуйте ещё раз.", "error")
    return redirect(url_for("main.index"))

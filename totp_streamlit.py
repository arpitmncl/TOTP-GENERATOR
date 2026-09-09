import streamlit as st
import pyotp
import time
from dotenv import load_dotenv
import os
from datetime import datetime


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# LOAD MULTIPLE TOTP ACCOUNTS
# ============================================================

totp_accounts = {}

i = 1

while True:

    name = os.getenv(f"TOTP_{i}_NAME")
    secret = os.getenv(f"TOTP_{i}_SECRET")

    # Stop when both are missing
    if not name and not secret:
        break

    if secret:

        account_name = name if name else f"Account {i}"

        try:
            totp_accounts[account_name] = pyotp.TOTP(secret.strip())

        except Exception as e:
            st.error(
                f"❌ Invalid TOTP secret for {account_name}: {e}"
            )

    i += 1


# ============================================================
# CHECK WHETHER ACCOUNTS EXIST
# ============================================================

if not totp_accounts:

    st.error(
        "❌ No TOTP accounts found.\n\n"
        "Please check your .env file."
    )

    st.stop()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TOTP Generator",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.html("""
<style>

    /* ======================================================
       MAIN BACKGROUND
       ====================================================== */

    [data-testid="stAppViewContainer"] {

        background:
            linear-gradient(
                135deg,
                #667eea 0%,
                #764ba2 25%,
                #f093fb 50%,
                #4facfe 75%,
                #00f2fe 100%
            );

        min-height: 100vh;
    }


    [data-testid="stHeader"] {
        background: transparent;
    }


    /* ======================================================
       TITLE
       ====================================================== */

    .totp-title {

        text-align: center;

        font-size: 42px;

        font-weight: 900;

        color: white;

        margin-top: 10px;

        margin-bottom: 35px;

        letter-spacing: 2px;

        text-shadow:
            0px 4px 15px rgba(0, 0, 0, 0.30);
    }


    /* ======================================================
       ACCOUNT CARD
       ====================================================== */

    .totp-card {

        background: rgba(255, 255, 255, 0.96);

        border-radius: 25px;

        padding: 30px 20px;

        text-align: center;

        box-shadow:
            0px 20px 40px rgba(0, 0, 0, 0.25);

        border:
            3px solid rgba(240, 147, 251, 0.50);

        margin-bottom: 20px;

        min-height: 235px;
    }


    /* ======================================================
       ACCOUNT NAME
       ====================================================== */

    .account-name {

        color: #764ba2;

        font-size: 24px;

        font-weight: 900;

        margin-bottom: 8px;

        letter-spacing: 1px;
    }


    /* ======================================================
       CURRENT TOKEN LABEL
       ====================================================== */

    .token-label {

        color: #764ba2;

        font-size: 14px;

        font-weight: 700;

        letter-spacing: 1px;

        margin-top: 5px;
    }


    /* ======================================================
       OTP
       ====================================================== */

    .otp-code {

        color: #667eea;

        font-size: 48px;

        font-weight: 900;

        font-family: "Courier New", monospace;

        letter-spacing: 10px;

        margin-top: 18px;

        margin-bottom: 5px;

        font-variant-numeric:
            tabular-nums;
    }


    /* ======================================================
       STATUS BADGES
       ====================================================== */

    .status-badge {

        display: inline-block;

        padding: 10px 22px;

        border-radius: 30px;

        color: white;

        font-size: 14px;

        font-weight: 900;

        letter-spacing: 1px;

        margin-top: 10px;

        box-shadow:
            0px 8px 20px rgba(0, 0, 0, 0.20);
    }


    .status-active {

        background:
            linear-gradient(
                135deg,
                #00f2fe,
                #4facfe
            );
    }


    .status-warning {

        background:
            linear-gradient(
                135deg,
                #f093fb,
                #f5576c
            );
    }


    .status-critical {

        background:
            linear-gradient(
                135deg,
                #ff6b6b,
                #ee5a6f
            );
    }


    /* ======================================================
       PROGRESS LABEL
       ====================================================== */

    .progress-label {

        text-align: center;

        color: #764ba2;

        font-weight: 800;

        font-size: 13px;

        margin-top: 10px;

        margin-bottom: 5px;

        letter-spacing: 1px;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .totp-footer {

        text-align: center;

        color: white;

        font-size: 14px;

        padding: 25px;

        margin-top: 20px;
    }

</style>
""")


# ============================================================
# TITLE
# ============================================================

st.html("""
<div class="totp-title">
    🔐 TOTP Generator Dashboard
</div>
""")


# ============================================================
# CURRENT TIME
# ============================================================

current_timestamp = time.time()

current_datetime = datetime.now()


# ============================================================
# ACCOUNT LIST
# ============================================================

account_list = list(totp_accounts.items())


# ============================================================
# DISPLAY 2 ACCOUNTS PER ROW
# ============================================================

for row_start in range(0, len(account_list), 2):

    row_accounts = account_list[row_start:row_start + 2]

    columns = st.columns(2)


    for column, (account_name, totp) in zip(
        columns,
        row_accounts
    ):

        with column:

            # ==================================================
            # GENERATE OTP
            # ==================================================

            current_otp = totp.now()


            # ==================================================
            # CALCULATE REMAINING TIME
            # ==================================================

            remaining_seconds = (
                totp.interval
                - (
                    int(current_timestamp)
                    % totp.interval
                )
            )


            # ==================================================
            # CALCULATE PROGRESS
            # ==================================================

            percentage = (
                remaining_seconds
                / totp.interval
            ) * 100


            # ==================================================
            # STATUS
            # ==================================================

            if remaining_seconds <= 5:

                status_class = "status-critical"

                status_text = "⚠️ EXPIRING SOON"


            elif remaining_seconds <= 10:

                status_class = "status-warning"

                status_text = "⏰ EXPIRES SOON"


            else:

                status_class = "status-active"

                status_text = "✅ ACTIVE"


            # ==================================================
            # ACCOUNT CARD
            # ==================================================

            account_card = f"""
            <div class="totp-card">

                <div class="account-name">
                    🔑 {account_name}
                </div>

                <div class="token-label">
                    CURRENT TOKEN
                </div>

                <div class="otp-code">
                    {current_otp}
                </div>

            </div>
            """

            st.html(account_card)


            # ==================================================
            # TIMER INFORMATION
            # ==================================================

            timer_col1, timer_col2 = st.columns(2)


            with timer_col1:

                st.metric(
                    label="⏱️ Expires In",
                    value=f"{remaining_seconds}s"
                )


            with timer_col2:

                st.metric(
                    label="🕐 Current Time",
                    value=current_datetime.strftime(
                        "%H:%M:%S"
                    )
                )


            # ==================================================
            # PROGRESS LABEL
            # ==================================================

            st.html("""
            <div class="progress-label">
                TOKEN EXPIRATION
            </div>
            """)


            # ==================================================
            # PROGRESS BAR
            # ==================================================

            st.progress(
                percentage / 100
            )


            # ==================================================
            # STATUS BADGE
            # ==================================================

            status_badge = f"""
            <div style="text-align: center;">

                <div class="status-badge {status_class}">
                    {status_text}
                </div>

            </div>
            """

            st.html(status_badge)


            # ==================================================
            # ADDITIONAL INFORMATION
            # ==================================================

            info_col1, info_col2 = st.columns(2)


            with info_col1:

                st.metric(
                    label="🔑 Token Lifetime",
                    value=f"{totp.interval}s"
                )


            with info_col2:

                st.metric(
                    label="📊 Fill %",
                    value=f"{int(percentage)}%"
                )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="totp-footer">

    <hr>

    <p>
        🔄 Dashboard auto-updates every second
    </p>

    <p>
        🔒 Tokens refresh automatically based on their TOTP interval
    </p>

    <p>
        ✨ Multi-Account Real-time TOTP Generator
    </p>

</div>
""")


# ============================================================
# AUTO REFRESH EVERY SECOND
# ============================================================

time.sleep(1)

st.rerun()

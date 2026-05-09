import streamlit as st
import mysql.connector
import pandas as pd
import altair as alt  # للرسم

# ---------------------------
#         MySQL CONNECT
# ---------------------------

def get_db_connection():
    # عدلي الباسورد / الداتابيس إذا احتجتي
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Remas555",
        database="DBproject",
        port=3307
    )

# ---------------------------
#     RUN SELECT QUERY
# ---------------------------

@st.cache_data(ttl=600)
def run_query(query, params=None):
    conn = get_db_connection()
    try:
        df = pd.read_sql(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        st.error(f"Query Error: {e}")
        return pd.DataFrame()

# ---------------------------
#  INSERT / UPDATE / DELETE
# ---------------------------

def execute_non_query(query, params=None):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params if params else ())
        conn.commit()
        cursor.close()
        conn.close()
        st.cache_data.clear()
        return True
    except Exception as e:
        conn.rollback()
        conn.close()
        st.error(f"Database Error: {e}")
        return False


# ---------------------------
#          LOGIN
# ---------------------------

def login():
    st.sidebar.header("🔑 User Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        query = "SELECT Role FROM Account WHERE Username=%s AND Password=%s"
        result = run_query(query, (username, password))
        
        if not result.empty:
            st.session_state['logged_in'] = True
            st.session_state['user_role'] = result.iloc[0, 0]
            st.session_state['username'] = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password.")


# ---------------------------
#        ADMIN VIEW
# ---------------------------

def admin_dashboard():
    st.title("🛡️ Admin Dashboard - CCMS")
    st.subheader(f"Welcome, {st.session_state['username']}!")

    # ------- Top metrics -------
    col1, col2, col3, col4 = st.columns(4)

    total_clubs = run_query("SELECT COUNT(*) AS c FROM Club").iloc[0, 0]
    active_clubs = run_query("SELECT COUNT(*) AS c FROM Club WHERE Status='Active'").iloc[0, 0]
    total_members = run_query("SELECT COUNT(*) AS c FROM Member WHERE Status='Active'").iloc[0, 0]
    total_admins = run_query("SELECT COUNT(*) AS c FROM Account WHERE Role='Admin'").iloc[0, 0]

    col1.metric("Total Clubs", total_clubs)
    col2.metric("Active Clubs", active_clubs)
    col3.metric("Active Members", total_members)
    col4.metric("Admin Accounts", total_admins)

    st.markdown("---")

    # ------- Analytics section with Altair charts -------
    chart_col1, chart_col2 = st.columns(2)

    # Members per club
    stats_df = run_query("""
        SELECT C.ClubName, COUNT(B.StudentID) AS MemberCount
        FROM Club C
        LEFT JOIN Belong_to B ON C.ClubID = B.ClubID
        GROUP BY C.ClubID, C.ClubName
        ORDER BY MemberCount DESC
    """)

    with chart_col1:
        if not stats_df.empty:
            st.subheader("📊 Members per Club")
            chart = (
                alt.Chart(stats_df)
                .mark_bar(size=35, color="#1f77b4")
                .encode(
                    x=alt.X("ClubName:N", sort="-y", title="Club"),
                    y=alt.Y("MemberCount:Q", title="Number of Members"),
                    tooltip=["ClubName", "MemberCount"]
                )
                .properties(
                    width=350,
                    height=300
                )
            )

            text = chart.mark_text(
                align="center",
                baseline="bottom",
                dy=-5,
                fontSize=11,
                color="black"
            ).encode(
                text="MemberCount:Q"
            )

            st.altair_chart(chart + text, use_container_width=True)
        else:
            st.info("No clubs found for statistics.")

    # Events by status
    events_stats = run_query("""
        SELECT Status, COUNT(*) AS Count
        FROM Event
        GROUP BY Status
    """)

    with chart_col2:
        if not events_stats.empty:
            st.subheader("📅 Events by Status")
            chart2 = (
                alt.Chart(events_stats)
                .mark_bar(size=35, color="#ff7f0e")
                .encode(
                    x=alt.X("Status:N", title="Status"),
                    y=alt.Y("Count:Q", title="Number of Events"),
                    tooltip=["Status", "Count"]
                )
                .properties(
                    width=350,
                    height=300
                )
            )

            text2 = chart2.mark_text(
                align="center",
                baseline="bottom",
                dy=-5,
                fontSize=11,
                color="black"
            ).encode(
                text="Count:Q"
            )

            st.altair_chart(chart2 + text2, use_container_width=True)
        else:
            st.info("No events found for statistics.")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Club Management", "Members", "Events"])

    # ---------------- CLUB CRUD ----------------
    with tab1:
        st.header("Club Management")

        clubs = run_query("SELECT ClubID, ClubName, PresidentName, Status FROM Club")
        st.dataframe(clubs, use_container_width=True)

        # Add new club
        with st.expander("➕ Add New Club"):
            with st.form("add_club_form", clear_on_submit=True):
                new_id = st.text_input("Club ID (e.g., C006)")
                new_name = st.text_input("Club Name")
                new_president = st.text_input("President Name")
                new_desc = st.text_area("Description")
                
                submitted = st.form_submit_button("Add Club")
                if submitted:
                    if new_id and new_name and new_president:
                        q = """
                        INSERT INTO Club (ClubID, ClubName, PresidentName, Status, Description)
                        VALUES (%s, %s, %s, 'Active', %s)
                        """
                        ok = execute_non_query(q, (new_id, new_name, new_president, new_desc))
                        if ok:
                            st.success("Club added!")
                            st.rerun()
                        else:
                            st.error("Failed to insert.")
                    else:
                        st.error("Fill all fields.")

        # Soft delete (Archive) club
        with st.expander("📁 Archive Club (Soft Delete)"):
            if not clubs.empty:
                active_only = clubs[clubs["Status"] == "Active"]
                if not active_only.empty:
                    selected = st.selectbox("Select active club to archive", active_only["ClubName"].tolist())
                    if st.button("Archive Club"):
                        cid = active_only[active_only["ClubName"] == selected]["ClubID"].iloc[0]
                        ok = execute_non_query("UPDATE Club SET Status='Inactive' WHERE ClubID=%s", (cid,))
                        if ok:
                            st.success("Club archived (status -> Inactive).")
                            st.rerun()
                else:
                    st.info("No active clubs to archive.")
            else:
                st.info("No clubs found.")

        # Hard delete option
        with st.expander("🗑️ Permanently Delete Club (Use with caution)"):
            if not clubs.empty:
                selected = st.selectbox("Select club to delete", clubs["ClubName"].tolist(), key="delete_club_select")
                if st.button("Delete Club", type="primary"):
                    cid = clubs[clubs["ClubName"] == selected]["ClubID"].iloc[0]

                    execute_non_query(
                        "DELETE FROM Participate WHERE EventID IN (SELECT EventID FROM Event WHERE ClubID=%s)",
                        (cid,)
                    )
                    execute_non_query("DELETE FROM Belong_to WHERE ClubID=%s", (cid,))
                    execute_non_query("DELETE FROM Event WHERE ClubID=%s", (cid,))
                    execute_non_query("DELETE FROM Club WHERE ClubID=%s", (cid,))

                    st.success("Deleted successfully!")
                    st.rerun()
            else:
                st.info("No clubs found.")

    # ---------------- MEMBERS ----------------
    with tab2:
        st.header("Members")

        # Search + filter UI
        col_search, col_status = st.columns([3, 1])
        search_text = col_search.text_input("Search by name or email")
        status_filter = col_status.selectbox("Status", ["All", "Active", "Inactive"])

        base_query = "SELECT StudentID, Name, Email, Status, JoinDate FROM Member WHERE 1=1"
        params = []

        if search_text:
            base_query += " AND (Name LIKE %s OR Email LIKE %s)"
            like = f"%{search_text}%"
            params.extend([like, like])

        if status_filter != "All":
            base_query += " AND Status=%s"
            params.append(status_filter)

        members_df = run_query(base_query, tuple(params) if params else None)
        st.dataframe(members_df, use_container_width=True)

        # Export CSV
        if not members_df.empty:
            csv = members_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download members as CSV",
                data=csv,
                file_name="members.csv",
                mime="text/csv",
            )

    # ---------------- EVENTS ----------------
    with tab3:
        st.header("Events")

        # Filters: by club + status
        clubs_for_filter = run_query("SELECT ClubID, ClubName FROM Club ORDER BY ClubName")
        col_club, col_status = st.columns([2, 1])

        club_options = ["All Clubs"]
        club_id_map = {}
        if not clubs_for_filter.empty:
            for _, row in clubs_for_filter.iterrows():
                club_options.append(row["ClubName"])
                club_id_map[row["ClubName"]] = row["ClubID"]

        selected_club = col_club.selectbox("Filter by club", club_options)
        event_status_filter = col_status.selectbox("Event Status", ["All", "Scheduled", "Completed", "Canceled"])

        q = """
        SELECT E.EventID, E.EventName, E.Date, E.Location, C.ClubName, E.Status
        FROM Event E
        JOIN Club C ON E.ClubID = C.ClubID
        WHERE 1=1
        """
        params = []

        if selected_club != "All Clubs":
            q += " AND C.ClubID=%s"
            params.append(club_id_map[selected_club])

        if event_status_filter != "All":
            q += " AND E.Status=%s"
            params.append(event_status_filter)

        q += " ORDER BY E.Date"

        events_df = run_query(q, tuple(params) if params else None)
        st.dataframe(events_df, use_container_width=True)

        # Export CSV
        if not events_df.empty:
            csv = events_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download events as CSV",
                data=csv,
                file_name="events.csv",
                mime="text/csv",
            )


# ---------------------------
#     PRESIDENT VIEW
# ---------------------------

def president_dashboard():
    st.title("👑 President Dashboard")

    q = """
    SELECT C.ClubID, C.ClubName, C.Status, C.Description
    FROM Club C 
    JOIN Account A ON C.PresidentName = (SELECT Name FROM Member WHERE StudentID=A.StudentID)
    WHERE A.Username=%s
    """
    info = run_query(q, (st.session_state['username'],))

    if info.empty:
        st.error("No club found.")
        return

    cid = info.iloc[0]["ClubID"]
    cname = info.iloc[0]["ClubName"]

    tab1, tab2 = st.tabs(["Club Summary", "Members"])

    with tab1:
        total = run_query(
            "SELECT COUNT(*) AS c FROM Belong_to WHERE ClubID=%s",
            (cid,)
        ).iloc[0, 0]
        col1, col2 = st.columns(2)
        col1.metric("Club", cname)
        col2.metric("Members", total)
        st.info(info.iloc[0]["Description"])

    with tab2:
        q = """
        SELECT M.StudentID, M.Name, M.Email, M.Status, B.JoinDate
        FROM Member M
        JOIN Belong_to B ON M.StudentID = B.StudentID
        WHERE B.ClubID=%s
        ORDER BY B.JoinDate
        """
        df = run_query(q, (cid,))
        st.dataframe(df, use_container_width=True)


# ---------------------------
#       MEMBER VIEW
# ---------------------------

def register_for_event_simple(student_id, event_id, event_name):
    q = "INSERT INTO Participate (StudentID, EventID) VALUES (%s, %s)"
    ok = execute_non_query(q, (student_id, event_id))
    if ok:
        st.success(f"Registered for {event_name}!")
        st.rerun()
    else:
        st.error("Already registered.")

def member_view():
    st.title("👤 Member View")

    q = "SELECT StudentID FROM Account WHERE Username=%s"
    df = run_query(q, (st.session_state['username'],))
    if df.empty:
        st.error("Student record not found.")
        return

    sid = df.iloc[0]["StudentID"]

    st.header("🤝 Your Clubs")
    q = """
    SELECT C.ClubName, C.PresidentName, C.Status, B.JoinDate
    FROM Club C
    JOIN Belong_to B ON C.ClubID = B.ClubID
    WHERE B.StudentID=%s
    """
    clubs = run_query(q, (sid,))
    st.dataframe(clubs, use_container_width=True)

    st.markdown("---")

    st.header("📝 Events Available")
    q = """
    SELECT E.EventID, E.EventName, E.Date, E.Location, C.ClubName
    FROM Event E 
    JOIN Club C ON E.ClubID = C.ClubID
    WHERE E.Status='Scheduled'
      AND E.EventID NOT IN (SELECT EventID FROM Participate WHERE StudentID=%s)
    ORDER BY E.Date
    """
    ev = run_query(q, (sid,))

    if not ev.empty:
        for idx, row in ev.iterrows():
            cols = st.columns([0.4, 0.15, 0.2, 0.2, 0.15])
            cols[0].write(row["EventName"])
            cols[1].write(row["Date"])
            cols[2].write(row["Location"])
            cols[3].write(row["ClubName"])
            if cols[4].button("Register", key=f"reg_{idx}"):
                register_for_event_simple(sid, row["EventID"], row["EventName"])
    else:
        st.info("No available events to register.")

    st.markdown("---")

    st.subheader("Your Registered Events")
    q = """
    SELECT E.EventName, E.Date, E.Location, C.ClubName, E.Status
    FROM Event E 
    JOIN Club C ON E.ClubID = C.ClubID
    JOIN Participate P ON E.EventID = P.EventID
    WHERE P.StudentID=%s
    ORDER BY E.Date
    """
    reg = run_query(q, (sid,))
    st.dataframe(reg, use_container_width=True)


# ---------------------------
#           MAIN
# ---------------------------

def main_app():
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        st.sidebar.write(f"Logged in as: {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()

        role = st.session_state['user_role']
        if role == "Admin":
            admin_dashboard()
        elif role == "President":
            president_dashboard()
        else:
            member_view()

    else:
        st.title("🏛️ College Club Management System")
        st.info("Please log in to continue")
        login()
        st.markdown("---")
        st.markdown("Test Accounts: Admin1/adminpass, Ibtihal_P/pass1, Ali_M/pass6")


if __name__ == "__main__":
    st.set_page_config(page_title="CCMS", layout="wide")
    main_app()

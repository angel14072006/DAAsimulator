import streamlit as st
import random
import time

# Page settings
st.set_page_config(page_title="Merge Sort Visualizer", page_icon="M", layout="wide", initial_sidebar_state="expanded")

# Simple CSS
st.markdown("""

<style>
/* ===== LIGHT ACADEMIC THEME ===== */
.stApp {
    background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 55%, #f7f1ff 100%);
    color: #1f2937;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

.hero {
    background: linear-gradient(135deg, #ffffff 0%, #eef4ff 100%);
    border: 1px solid #dbe5f5;
    border-radius: 22px;
    padding: 30px 34px;
    margin-bottom: 24px;
    box-shadow: 0 8px 30px rgba(67, 88, 120, 0.10);
}

.hero h1 {
    margin: 0;
    color: #243b64;
    font-size: 2.55rem;
    font-weight: 800;
}

.hero p {
    margin: 8px 0 0;
    color: #64748b;
    font-size: 1.05rem;
}

.section-title {
    color: #334e7c;
    font-size: 1.45rem;
    font-weight: 750;
    margin: 18px 0 12px;
}

.info-card {
    background: #ffffff;
    border: 1px solid #dce6f4;
    border-radius: 16px;
    padding: 18px 20px;
    margin: 12px 0;
    box-shadow: 0 5px 18px rgba(67, 88, 120, 0.07);
}

.info-card h3 {
    color: #334e7c;
    margin: 0 0 8px;
}

.info-card p {
    color: #5f6f86;
    margin: 0;
    line-height: 1.55;
}

.array-container {
    background: #ffffff;
    border: 1px solid #dce6f4;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 5px 18px rgba(67, 88, 120, 0.07);
    margin: 10px 0 20px;
}

.array-label {
    color: #64748b;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}


/* Compatibility styles for the simulator's original array renderer */
.array {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    padding: 8px 0;
}

.box {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 52px;
    height: 52px;
    padding: 0 10px;
    border-radius: 12px;
    background: #edf3ff;
    border: 2px solid #cbdaf2;
    color: #29446f;
    font-size: 1.15rem;
    font-weight: 750;
    box-sizing: border-box;
}

.box.compare {
    background: #fff3df;
    border-color: #f0b35b;
    color: #9a5a00;
}

.box.result {
    background: #e9f8ef;
    border-color: #55ad76;
    color: #1f6638;
}

.array-box {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 52px;
    height: 52px;
    margin: 5px;
    border-radius: 12px;
    background: #edf3ff;
    border: 2px solid #cbdaf2;
    color: #29446f;
    font-size: 1.15rem;
    font-weight: 750;
}

.array-box.compare {
    background: #fff3df;
    border-color: #f0b35b;
    color: #9a5a00;
}

.array-box.selected {
    background: #e9f8ef;
    border-color: #72c58c;
    color: #23633b;
}

.array-box.done {
    background: #e9f8ef;
    border-color: #55ad76;
    color: #1f6638;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #dce6f4;
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(67, 88, 120, 0.06);
}

.metric-value {
    color: #31598f;
    font-size: 1.65rem;
    font-weight: 800;
}

.metric-label {
    color: #718096;
    font-size: 0.82rem;
    margin-top: 3px;
}

.stage-card {
    background: #ffffff;
    border-left: 5px solid #6c8fd3;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0;
    box-shadow: 0 4px 14px rgba(67, 88, 120, 0.06);
}

.stage-card strong {
    color: #334e7c;
}

.stage-card span {
    color: #66758a;
}

.footer {
    text-align: center;
    color: #8190a5;
    font-size: 0.85rem;
    padding: 28px 0 10px;
    border-top: 1px solid #dce6f4;
    margin-top: 35px;
}

/* Streamlit controls */
.stButton > button {
    border-radius: 10px;
    border: 1px solid #cbdaf2;
    background: #ffffff;
    color: #31598f;
    font-weight: 650;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #7b9bd3;
    background: #f2f6ff;
    color: #274a7a;
}

[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #dce6f4;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #334e7c;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #596b82;
}

.stTextInput > div > div > input {
    background: #ffffff;
    border: 1px solid #cbdaf2;
    color: #26364d;
}

.stTextInput > div > div > input:focus {
    border-color: #7192cc;
    box-shadow: 0 0 0 1px #7192cc;
}

.stProgress > div > div > div > div {
    background: #6c8fd3;
}
</style>

""", unsafe_allow_html=True)


# -------------------------------------------------------
# Session variables
# -------------------------------------------------------

if "frames" not in st.session_state:
    st.session_state.frames = []

if "step" not in st.session_state:
    st.session_state.step = 0

if "array" not in st.session_state:
    st.session_state.array = [8, 3, 5, 2, 7, 4, 6, 1]

if "auto" not in st.session_state:
    st.session_state.auto = False


# -------------------------------------------------------
# Merge Sort frame generation
# -------------------------------------------------------

def create_frames(array):

    frames = []
    comparisons = 0
    merges = 0

    frames.append({
        "stage": "Initial Array",
        "description": "The array before sorting begins.",
        "array": array.copy(),
        "left": [],
        "right": [],
        "result": [],
        "compare": [],
        "comparisons": 0,
        "merges": 0
    })

    def merge_sort(arr):

        nonlocal comparisons, merges

        if len(arr) <= 1:
            return arr

        middle = len(arr) // 2

        left = arr[:middle]
        right = arr[middle:]

        # Show division
        frames.append({
            "stage": "Division",
            "description": "The array is divided into two smaller parts.",
            "array": arr.copy(),
            "left": left.copy(),
            "right": right.copy(),
            "result": [],
            "compare": [],
            "comparisons": comparisons,
            "merges": merges
        })

        left = merge_sort(left)
        right = merge_sort(right)

        merges += 1

        frames.append({
            "stage": "Merging",
            "description": "The two sorted parts are ready to be merged.",
            "array": arr.copy(),
            "left": left.copy(),
            "right": right.copy(),
            "result": [],
            "compare": [],
            "comparisons": comparisons,
            "merges": merges
        })

        i = 0
        j = 0
        merged = []

        while i < len(left) and j < len(right):

            comparisons += 1

            frames.append({
                "stage": "Comparison",
                "description":
                    f"Comparing {left[i]} and {right[j]}. "
                    f"The smaller value will be selected.",
                "array": arr.copy(),
                "left": left[i:],
                "right": right[j:],
                "result": merged.copy(),
                "compare": [left[i], right[j]],
                "comparisons": comparisons,
                "merges": merges
            })

            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

            frames.append({
                "stage": "Selecting Element",
                "description":
                    f"The smaller element has been added to the merged portion.",
                "array": arr.copy(),
                "left": left[i:],
                "right": right[j:],
                "result": merged.copy(),
                "compare": [],
                "comparisons": comparisons,
                "merges": merges
            })

        # Add remaining elements from left
        while i < len(left):

            merged.append(left[i])

            frames.append({
                "stage": "Adding Remaining Element",
                "description":
                    f"{left[i]} remains in the left part and is added to the result.",
                "array": arr.copy(),
                "left": left[i + 1:],
                "right": right[j:],
                "result": merged.copy(),
                "compare": [],
                "comparisons": comparisons,
                "merges": merges
            })

            i += 1

        # Add remaining elements from right
        while j < len(right):

            merged.append(right[j])

            frames.append({
                "stage": "Adding Remaining Element",
                "description":
                    f"{right[j]} remains in the right part and is added to the result.",
                "array": arr.copy(),
                "left": left[i:],
                "right": right[j + 1:],
                "result": merged.copy(),
                "compare": [],
                "comparisons": comparisons,
                "merges": merges
            })

            j += 1

        frames.append({
            "stage": "Merge Completed",
            "description":
                "The two parts have been merged into one sorted portion.",
            "array": arr.copy(),
            "left": [],
            "right": [],
            "result": merged.copy(),
            "compare": [],
            "comparisons": comparisons,
            "merges": merges
        })

        return merged

    sorted_array = merge_sort(array.copy())

    frames.append({
        "stage": "Sorting Completed",
        "description": "All elements have been sorted successfully.",
        "array": sorted_array.copy(),
        "left": [],
        "right": [],
        "result": sorted_array.copy(),
        "compare": [],
        "comparisons": comparisons,
        "merges": merges
    })

    return frames


# -------------------------------------------------------
# Display array
# -------------------------------------------------------

def show_array(values, highlighted=None, green=False):

    if highlighted is None:
        highlighted = []

    boxes = []

    for value in values:
        if value in highlighted:
            style = "box compare"
        elif green:
            style = "box result"
        else:
            style = "box"

        boxes.append(f'<div class="{style}">{value}</div>')

    html = '<div class="array">' + "".join(boxes) + '</div>'

    st.markdown(html, unsafe_allow_html=True)


# -------------------------------------------------------
# Title
# -------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="title">Merge Sort Visualizer</div>
        <div class="subtitle">Design and Analysis of Algorithms • Interactive Divide & Conquer Simulator</div>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="info-card">
        <b>How it works:</b> Enter an array, start the simulation, and move through
        each stage of Merge Sort — division, comparison, selection, merging, and the
        final sorted array.
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    st.header("Simulation Controls")

    input_array = st.text_input(
        "Enter array elements",
        value=", ".join(map(str, st.session_state.array))
    )

    if st.button("Start Simulation", use_container_width=True):

        try:

            numbers = [
                int(x.strip())
                for x in input_array.split(",")
                if x.strip()
            ]

            if len(numbers) < 2:
                st.error("Please enter at least two numbers.")

            elif len(numbers) > 12:
                st.error("Please enter a maximum of 12 numbers.")

            else:

                st.session_state.array = numbers
                st.session_state.frames = create_frames(numbers)
                st.session_state.step = 0
                st.session_state.auto = False

                st.rerun()

        except ValueError:

            st.error("Enter numbers separated by commas.")

    if st.button("Generate Random Array", use_container_width=True):

        numbers = random.sample(range(1, 50), 8)

        st.session_state.array = numbers
        st.session_state.frames = create_frames(numbers)
        st.session_state.step = 0
        st.session_state.auto = False

        st.rerun()

    if st.button("Reset", use_container_width=True):

        st.session_state.array = [8, 3, 5, 2, 7, 4, 6, 1]
        st.session_state.frames = []
        st.session_state.step = 0
        st.session_state.auto = False

        st.rerun()

    st.divider()

    st.header("Algorithm Information")

    st.write("""
    Merge Sort is based on the Divide and Conquer technique.

    The algorithm works in three main stages:

    1. Divide the array into smaller parts.
    2. Recursively sort the smaller parts.
    3. Merge the sorted parts.
    """)

    st.write("Time Complexity: O(n log n)")
    st.write("Space Complexity: O(n)")


# -------------------------------------------------------
# No simulation yet
# -------------------------------------------------------

if not st.session_state.frames:

    st.info(
        "Enter an array in the sidebar and click "
        "'Start Simulation' to begin."
    )

    st.subheader("How the simulator works")

    st.write("""
    The simulator demonstrates the complete Merge Sort process.

    Initial Array
        ↓
    Division
        ↓
    Recursive Subdivision
        ↓
    Element Comparison
        ↓
    Merging
        ↓
    Final Sorted Array
    """)

    st.stop()


# -------------------------------------------------------
# Current frame
# -------------------------------------------------------

frames = st.session_state.frames
step = st.session_state.step

frame = frames[step]


# -------------------------------------------------------
# Progress
# -------------------------------------------------------

st.progress((step + 1) / len(frames))

st.write(
    f"Step {step + 1} of {len(frames)}"
)


# -------------------------------------------------------
# Current stage
# -------------------------------------------------------

st.markdown(
    f"""
    <div class="stage-card">
        <h2 style="margin:0 0 8px 0;">{frame["stage"]}</h2>
        <p style="margin:0; color:#c7d2fe;">{frame["description"]}</p>
    </div>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------------
# Initial array
# -------------------------------------------------------

if frame["stage"] == "Initial Array":

    st.subheader("Original Array")

    show_array(frame["array"])


# -------------------------------------------------------
# Division
# -------------------------------------------------------

elif frame["stage"] == "Division":

    st.subheader("Dividing the Array")

    col1, col2 = st.columns(2)

    with col1:

        st.write("Left Part")

        show_array(frame["left"])

    with col2:

        st.write("Right Part")

        show_array(frame["right"])


# -------------------------------------------------------
# Merging
# -------------------------------------------------------

elif frame["stage"] == "Merging":

    st.subheader("Sorted Parts")

    col1, col2 = st.columns(2)

    with col1:

        st.write("Left Sorted Part")

        show_array(frame["left"])

    with col2:

        st.write("Right Sorted Part")

        show_array(frame["right"])


# -------------------------------------------------------
# Comparison
# -------------------------------------------------------

elif frame["stage"] == "Comparison":

    st.subheader("Comparing Elements")

    if len(frame["compare"]) == 2:

        first = frame["compare"][0]
        second = frame["compare"][1]

        st.markdown(
            f"""
            <div class="section">
                <h2 class="center">
                    {first} compared with {second}
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("Left part")

    show_array(frame["left"], frame["compare"])

    st.write("Right part")

    show_array(frame["right"], frame["compare"])

    if frame["result"]:

        st.write("Merged result so far")

        show_array(frame["result"], green=True)


# -------------------------------------------------------
# Selecting
# -------------------------------------------------------

elif frame["stage"] == "Selecting Element":

    st.subheader("Selecting Smaller Element")

    show_array(frame["result"], green=True)


# -------------------------------------------------------
# Remaining element
# -------------------------------------------------------

elif frame["stage"] == "Adding Remaining Element":

    st.subheader("Adding Remaining Element")

    show_array(frame["result"], green=True)


# -------------------------------------------------------
# Merge completed
# -------------------------------------------------------

elif frame["stage"] == "Merge Completed":

    st.subheader("Sorted Portion")

    show_array(frame["result"], green=True)


# -------------------------------------------------------
# Final result
# -------------------------------------------------------

elif frame["stage"] == "Sorting Completed":

    st.success("Sorting completed.")

    st.subheader("Final Sorted Array")

    show_array(frame["result"], green=True)


# -------------------------------------------------------
# Statistics
# -------------------------------------------------------

st.divider()

st.subheader("Simulation Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Current Step", f"{step + 1}/{len(frames)}")

with col2:
    st.metric("Comparisons", frame["comparisons"])

with col3:
    st.metric("Merge Operations", frame["merges"])

with col4:
    st.metric("Number of Elements", len(st.session_state.array))


# -------------------------------------------------------
# Navigation
# -------------------------------------------------------

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "Previous",
        disabled=(step == 0),
        use_container_width=True
    ):

        st.session_state.step -= 1
        st.rerun()


with col2:

    if st.button(
        "Next",
        disabled=(step >= len(frames) - 1),
        use_container_width=True
    ):

        st.session_state.step += 1
        st.rerun()


with col3:

    if st.button(
        "Auto Play",
        disabled=(step >= len(frames) - 1),
        use_container_width=True
    ):

        st.session_state.auto = True


# -------------------------------------------------------
# Auto play
# -------------------------------------------------------

if (
    st.session_state.auto
    and step < len(frames) - 1
):

    time.sleep(1)

    st.session_state.step += 1

    st.rerun()


# -------------------------------------------------------
# Pseudocode
# -------------------------------------------------------

st.divider()

with st.expander("Merge Sort Pseudocode"):

    st.code("""
        MERGE_SORT(A, low, high)

            if low < high

                mid = (low + high) / 2

                MERGE_SORT(A, low, mid)

                MERGE_SORT(A, mid + 1, high)

                MERGE(A, low, mid, high)
    """, language="text")


# -------------------------------------------------------
# Complexity
# -------------------------------------------------------

with st.expander("Complexity Analysis"):

    st.write("""
    Best Case: O(n log n)

    Average Case: O(n log n)

    Worst Case: O(n log n)

    Space Complexity: O(n)
    """)


# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="footer">
        Merge Sort Visualizer • Design and Analysis of Algorithms<br>
        Interactive educational prototype
    </div>
    """,
    unsafe_allow_html=True
)
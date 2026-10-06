import streamlit as st
import random
import time

# Page settings
st.set_page_config(
    page_title="Merge Sort Simulator",
    layout="wide"
)

# Simple CSS
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    margin-bottom: 30px;
}

.array {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin: 20px 0;
}

.box {
    width: 55px;
    height: 55px;
    border: 2px solid #444;
    border-radius: 8px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    font-weight: bold;
}

.compare {
    background-color: #fff0b3;
    border: 3px solid #d99a00;
}

.result {
    background-color: #d9f2d9;
    border: 2px solid #4c8c4a;
}

.section {
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin: 10px 0;
}

.center {
    text-align: center;
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

    html = '<div class="array">'

    for value in values:

        if value in highlighted:
            style = "box compare"
        elif green:
            style = "box result"
        else:
            style = "box"

        html += f"""
        <div class="{style}">
            {value}
        </div>
        """

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)


# -------------------------------------------------------
# Title
# -------------------------------------------------------

st.markdown(
    '<div class="title">Merge Sort Simulator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'An interactive demonstration of the Merge Sort algorithm'
    '</div>',
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

st.header(frame["stage"])

st.write(frame["description"])


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
    <p style="text-align:center;">
    Merge Sort Simulator | Design and Analysis of Algorithms
    </p>
    """,
    unsafe_allow_html=True
)
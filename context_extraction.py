# Full code block to copy-paste

import re

def extract_docs_from_context(parameters, documentation_path):
    """
    Extracts parameter documentation when the primary method fails. 
    It captures more context around the parameter.
    """
    with open(documentation_path, 'r') as doc_file:
        doc_content = doc_file.read()

    param_docs = {}
    
    for param in parameters:
        escaped_param = re.escape(param.split("=")[0].strip())
        
        # Look for the parameter and capture some lines before and after it
        pattern = r".{0,500}" + escaped_param + r".{0,500}"
        
        search_result = re.search(pattern, doc_content, re.IGNORECASE | re.DOTALL)
        
        if search_result:
            snippet = search_result.group(0).strip()
            snippet = re.sub(r'\s+', ' ', snippet)
            param_docs[param] = snippet
        else:
            param_docs[param] = "Not Found in Documentation"
    
    return param_docs

def best_extract_relevant_docs_v18(parameters, documentation_path):
    """
    Extract the relevant documentation parts for the given parameters.
    This function attempts to get the primary description of each parameter from the documentation.
    """
    with open(documentation_path, 'r') as doc_file:
        doc_content = doc_file.read()

    param_docs = {}
    
    # Define a list of common parameter endings to help refine the extraction
    common_endings = [
        r"\n\n", r"\n%", r"\n#", r"\n[^\n]*\s{2,}[A-Z]", r"\n[^\n]*\s{2,}[0-9]", r"\n[^\n]*\s{2,}[a-z]",
        r"\.\s", r"\;\s", r"\!\s"
    ]

    for param in parameters:
        # Escape any special characters in the parameter name
        escaped_param = re.escape(param.split("=")[0].strip())
        
        # Construct a search pattern to better match parameters with minimal descriptions
        # or those mentioned in list formats
        pattern = r"(" + escaped_param + r"\s{0,5}[:\(\)].*?)(?=" + "|".join(common_endings) + r"|\n" + escaped_param + r")"
        
        # Search for the pattern in the documentation
        search_result = re.search(pattern, doc_content, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        
        # Special handling for OPENMP
        if param == "OPENMP" and not search_result:
            openmp_pattern = r"(OPENMP\s{0,5}.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n)"
            search_result = re.search(openmp_pattern, doc_content, re.IGNORECASE | re.MULTILINE)
        
        if search_result:
            # Store the found snippet and clean it up (removing multiple spaces, etc.)
            snippet = search_result.group(0).strip()
            snippet = re.sub(r'\s+', ' ', snippet)
            param_docs[param] = snippet
        else:
            # Use the context extraction function if the primary method fails
            context_docs = extract_docs_from_context([param], documentation_path)
            param_docs[param] = context_docs[param]

    return param_docs

"""
# Test the functions with the provided parameters
additional_zel_params = [
    "TurbDrive_TimeBetTurbSpectrum",
    "Softening_Type5",
    "Effective_Kernel_NeighborNumber",
    "Maximum_Timestep_Allowed"
]

additional_config_params = [
    "MERGESPLIT_HARDCODE_MIN_MASS=(1.0e-7)",
    "OUTPUT_TURB_DIFF_DYNAMIC_ERROR",
    "RT_SOURCES=1+16+32",
    "HYDRO_MESHLESS_FINITE_MASS"
]

# Extracting documentation snippets for the mentioned parameters using the further refined extraction logic
refined_zel_docs_v18 = best_extract_relevant_docs_v18(additional_zel_params, "./GIZMO_Documentation.txt")
refined_config_docs_v18 = best_extract_relevant_docs_v18(additional_config_params, "./GIZMO_Documentation.txt")

# Print the results
print("Documentation for zel.params parameters:")
for param, doc in refined_zel_docs_v18.items():
    print(f"{param}: {doc}\n")

print("\nDocumentation for Config.sh parameters:")
for param, doc in refined_config_docs_v18.items():
    print(f"{param}: {doc}\n")
"""

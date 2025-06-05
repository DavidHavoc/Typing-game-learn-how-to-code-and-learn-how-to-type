import os
from huggingface_hub import InferenceClient
import random

class CodeGenerator:
    """
    A class to generate code snippets from the DeepSeek-R1-0528 model
    for different programming languages.
    """
    
    def __init__(self):
        """Initialize the code generator with the Hugging Face client."""
        os.environ["HF_TOKEN"] = "hf_KEY"
        
        # Initialize the client
        try:
            self.client = InferenceClient(
                provider="sambanova",
                api_key=os.environ["HF_TOKEN"],
            )
            self.is_api_available = True
        except Exception as e:
            print(f"Error initializing Hugging Face client: {e}")
            self.is_api_available = False
    
    def generate_code(self, language):
        """
        Generate code snippet for the specified programming language.
        
        Args:
            language (str): Programming language (py, cpp, java, rust, javascript)
            
        Returns:
            str: Generated code snippet
        """
        if not self.is_api_available:
            return self._get_sample_code(language)
            
        try:
            # Map short language codes to full names for better prompts
            language_map = {
                "py": "Python",
                "cpp": "C++",
                "java": "Java",
                "rust": "Rust",
                "javascript": "JavaScript"
            }
            
            full_language = language_map.get(language, language)
            
            # Create a prompt that will generate code of appropriate length
            prompt = f"Write a {full_language} program that demonstrates a useful algorithm or data structure. The code should be well-commented, educational, and between 175-200 lines long. Do not include any explanations outside the code."
            
            # Generate the code
            completion = self.client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1-0528",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )
            
            # Extract the code from the response
            generated_code = completion.choices[0].message.content
            
            # Clean up the code (remove markdown code blocks if present)
            if "```" in generated_code:
                code_blocks = generated_code.split("```")
                for block in code_blocks:
                    if language in block or full_language.lower() in block.lower():
                        # Found the right code block, extract the code
                        lines = block.split("\n")
                        # Remove the language identifier line
                        return "\n".join(lines[1:])
                
                # If we didn't find a specific language block, return the first code block
                return generated_code.split("```")[1].split("\n", 1)[1]
            
            return generated_code
            
        except Exception as e:
            print(f"Error generating code: {e}")
            return self._get_sample_code(language)
    
    def _get_sample_code(self, language):
        """
        Provide sample code when API is not available.
        
        Args:
            language (str): Programming language
            
        Returns:
            str: Sample code for the specified language
        """
        # Define sample code for each language
        py_sample = """# Binary Search implementation in Python
def binary_search(arr, target):
    '''
    Performs binary search on a sorted array.
    
    Args:
        arr: A sorted list of elements
        target: The element to search for
        
    Returns:
        int: The index of the target element, or -1 if not found
    '''
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        # Check if target is present at mid
        if arr[mid] == target:
            return mid
        
        # If target is greater, ignore left half
        elif arr[mid] < target:
            left = mid + 1
        
        # If target is smaller, ignore right half
        else:
            right = mid - 1
    
    # Element is not present in array
    return -1

# Example usage
def main():
    # Test array
    sorted_array = [2, 3, 4, 10, 40, 50, 70, 80, 90, 100]
    
    # Element to search
    target = 10
    
    # Function call
    result = binary_search(sorted_array, target)
    
    if result != -1:
        print(f"Element {target} is present at index {result}")
    else:
        print(f"Element {target} is not present in array")
    
    # Additional examples
    for test_target in [2, 30, 70, 100, 110]:
        result = binary_search(sorted_array, test_target)
        if result != -1:
            print(f"Element {test_target} is present at index {result}")
        else:
            print(f"Element {test_target} is not present in array")

if __name__ == "__main__":
    main()
"""

        cpp_sample = """// Binary Search implementation in C++
#include <iostream>
#include <vector>

/**
 * Performs binary search on a sorted array.
 * 
 * @param arr The sorted array to search in
 * @param target The element to search for
 * @return The index of the target element, or -1 if not found
 */
int binarySearch(const std::vector<int>& arr, int target) {
    int left = 0;
    int right = arr.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        // Check if target is present at mid
        if (arr[mid] == target)
            return mid;
        
        // If target is greater, ignore left half
        if (arr[mid] < target)
            left = mid + 1;
        
        // If target is smaller, ignore right half
        else
            right = mid - 1;
    }
    
    // Element is not present in array
    return -1;
}

int main() {
    // Test array
    std::vector<int> sortedArray = {2, 3, 4, 10, 40, 50, 70, 80, 90, 100};
    
    // Element to search
    int target = 10;
    
    // Function call
    int result = binarySearch(sortedArray, target);
    
    if (result != -1)
        std::cout << "Element " << target << " is present at index " << result << std::endl;
    else
        std::cout << "Element " << target << " is not present in array" << std::endl;
    
    // Additional examples
    int testTargets[] = {2, 30, 70, 100, 110};
    for (int testTarget : testTargets) {
        result = binarySearch(sortedArray, testTarget);
        if (result != -1)
            std::cout << "Element " << testTarget << " is present at index " << result << std::endl;
        else
            std::cout << "Element " << testTarget << " is not present in array" << std::endl;
    }
    
    return 0;
}
"""

        java_sample = """// Binary Search implementation in Java
public class BinarySearch {
    /**
     * Performs binary search on a sorted array.
     * 
     * @param arr The sorted array to search in
     * @param target The element to search for
     * @return The index of the target element, or -1 if not found
     */
    public static int binarySearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            // Check if target is present at mid
            if (arr[mid] == target)
                return mid;
            
            // If target is greater, ignore left half
            if (arr[mid] < target)
                left = mid + 1;
            
            // If target is smaller, ignore right half
            else
                right = mid - 1;
        }
        
        // Element is not present in array
        return -1;
    }
    
    public static void main(String[] args) {
        // Test array
        int[] sortedArray = {2, 3, 4, 10, 40, 50, 70, 80, 90, 100};
        
        // Element to search
        int target = 10;
        
        // Function call
        int result = binarySearch(sortedArray, target);
        
        if (result != -1)
            System.out.println("Element " + target + " is present at index " + result);
        else
            System.out.println("Element " + target + " is not present in array");
        
        // Additional examples
        int[] testTargets = {2, 30, 70, 100, 110};
        for (int testTarget : testTargets) {
            result = binarySearch(sortedArray, testTarget);
            if (result != -1)
                System.out.println("Element " + testTarget + " is present at index " + result);
            else
                System.out.println("Element " + testTarget + " is not present in array");
        }
    }
}
"""

        rust_sample = """// Binary Search implementation in Rust
fn binary_search(arr: &[i32], target: i32) -> Option<usize> {
    let mut left = 0;
    let mut right = arr.len();
    
    while left < right {
        let mid = left + (right - left) / 2;
        
        // Check if target is present at mid
        if arr[mid] == target {
            return Some(mid);
        }
        
        // If target is greater, ignore left half
        if arr[mid] < target {
            left = mid + 1;
        }
        // If target is smaller, ignore right half
        else {
            right = mid;
        }
    }
    
    // Element is not present in array
    None
}

fn main() {
    // Test array
    let sorted_array = [2, 3, 4, 10, 40, 50, 70, 80, 90, 100];
    
    // Element to search
    let target = 10;
    
    // Function call
    match binary_search(&sorted_array, target) {
        Some(index) => println!("Element {} is present at index {}", target, index),
        None => println!("Element {} is not present in array", target),
    }
    
    // Additional examples
    let test_targets = [2, 30, 70, 100, 110];
    for &test_target in &test_targets {
        match binary_search(&sorted_array, test_target) {
            Some(index) => println!("Element {} is present at index {}", test_target, index),
            None => println!("Element {} is not present in array", test_target),
        }
    }
}
"""

        javascript_sample = """// Binary Search implementation in JavaScript
/**
 * Performs binary search on a sorted array.
 * 
 * @param {Array} arr - The sorted array to search in
 * @param {number} target - The element to search for
 * @return {number} - The index of the target element, or -1 if not found
 */
function binarySearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;
    
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        
        // Check if target is present at mid
        if (arr[mid] === target) {
            return mid;
        }
        
        // If target is greater, ignore left half
        if (arr[mid] < target) {
            left = mid + 1;
        }
        // If target is smaller, ignore right half
        else {
            right = mid - 1;
        }
    }
    
    // Element is not present in array
    return -1;
}

// Test array
const sortedArray = [2, 3, 4, 10, 40, 50, 70, 80, 90, 100];

// Element to search
const target = 10;

// Function call
const result = binarySearch(sortedArray, target);

if (result !== -1) {
    console.log(`Element ${target} is present at index ${result}`);
} else {
    console.log(`Element ${target} is not present in array`);
}

// Additional examples
const testTargets = [2, 30, 70, 100, 110];
for (const testTarget of testTargets) {
    const testResult = binarySearch(sortedArray, testTarget);
    if (testResult !== -1) {
        console.log(`Element ${testTarget} is present at index ${testResult}`);
    } else {
        console.log(`Element ${testTarget} is not present in array`);
    }
}
"""

        # Map language codes to sample code
        samples = {
            "py": py_sample,
            "cpp": cpp_sample,
            "java": java_sample,
            "rust": rust_sample,
            "javascript": javascript_sample
        }
        
        return samples.get(language, samples["py"])

# Test the code generator
if __name__ == "__main__":
    generator = CodeGenerator()
    for lang in ["py", "cpp", "java", "rust", "javascript"]:
        print(f"\nGenerating {lang} code:")
        code = generator.generate_code(lang)
        print(f"Generated {len(code.splitlines())} lines of {lang} code")

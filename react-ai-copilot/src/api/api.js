/**
 * API Client for Flask AI Copilot Backend
 * Handles all HTTP requests using Axios
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes for module generation
});

/**
 * Generate a learning module from instructor prompt
 * @param {string} instructorPrompt - The instructor's prompt (e.g., "RAG module, intermediate, 5 days")
 * @returns {Promise<Object>} Module data with module_name, file_tree, and zip_path
 */
export const generateModule = async (instructorPrompt) => {
  try {
    console.log('[API] POST /generate-module with prompt:', instructorPrompt);
    const response = await api.post('/generate-module', {
      instructor_prompt: instructorPrompt,
    });

    console.log('[API] Response status:', response.status);
    console.log('[API] Response data keys:', Object.keys(response.data || {}));

    const { module_name, files, status } = response.data || {};
    
    // Validate response structure
    if (status === 'error') {
      throw new Error(response.data?.message || 'Server returned an error');
    }
    
    if (!module_name) {
      console.error('[API] Missing module_name in response:', response.data);
      throw new Error('Invalid response: missing module_name');
    }
    
    if (!files) {
      console.warn('[API] Missing files in response, using empty object');
      return { module_name, files: {} };
    }
    
    if (typeof files !== 'object') {
      console.error('[API] Invalid files type:', typeof files);
      throw new Error('Invalid response: files must be an object');
    }

    console.log('[API] Successfully parsed response:', {
      module_name,
      fileCount: Object.keys(files).length
    });

    return { module_name, files };
  } catch (error) {
    console.error('[API] Error details:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status
    });

    if (error.message && error.message.includes('Network Error')) {
      console.error('[API] CORS issue between React and Flask');
      throw new Error('Network error. Please check if the backend is running and CORS is configured.');
    }

    if (error.response) {
      // Server responded with error status
      const errorData = error.response.data || {};
      const errorMessage = errorData.message || errorData.error || 'Failed to generate module';
      console.error('[API] Server error:', errorMessage);
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request made but no response
      console.error('[API] No response from server');
      throw new Error('No response from server. Is the backend running on http://localhost:5000?');
    } else {
      // Error setting up request
      throw new Error(error.message || 'Failed to generate module');
    }
  }
};

/**
 * Download a module as ZIP file
 * @param {string} moduleName - Name of the module to download
 * @returns {Promise<boolean>} True if download succeeded
 */
export const downloadModule = async (moduleName) => {
  try {
    const response = await api.get('/download-module', {
      params: { module: moduleName },
      responseType: 'blob', // Important for file downloads
    });
    
    // Verify we got a blob (ZIP file)
    if (!(response.data instanceof Blob)) {
      // Try to parse as JSON error
      const text = await response.data.text();
      try {
        const errorData = JSON.parse(text);
        throw new Error(errorData.error || errorData.message || 'Failed to download module');
      } catch {
        throw new Error('Invalid response from server');
      }
    }
    
    // Verify blob size (ZIP files should be > 0 bytes)
    const blob = new Blob([response.data], { type: 'application/zip' });
    if (blob.size === 0) {
      throw new Error('Downloaded file is empty');
    }
    
    console.log('[Download] ZIP file size:', blob.size, 'bytes');
    
    // Create blob URL
    const url = window.URL.createObjectURL(blob);
    
    // Create temporary download link
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${moduleName}.zip`);
    link.style.display = 'none';
    
    // Trigger download
    document.body.appendChild(link);
    link.click();
    
    // Cleanup
    setTimeout(() => {
      if (document.body.contains(link)) {
        document.body.removeChild(link);
      }
      window.URL.revokeObjectURL(url);
    }, 100);
    
    return true;
  } catch (error) {
    // Handle blob response errors (when server returns JSON error)
    if (error.response && error.response.data instanceof Blob) {
      try {
        const text = await error.response.data.text();
        const errorData = JSON.parse(text);
        throw new Error(errorData.error || errorData.message || 'Failed to download module');
      } catch (parseError) {
        throw new Error('Failed to download module');
      }
    }
    
    if (error.message && error.message.includes('Network Error')) {
      console.error('CORS issue between React and Flask');
      throw new Error('CORS issue between React and Flask');
    }

    if (error.response) {
      // Handle JSON error responses
      const errorMessage = error.response.data?.error || error.response.data?.message || 'Failed to download module';
      throw new Error(errorMessage);
    } else if (error.request) {
      console.error('CORS issue between React and Flask');
      throw new Error('No response from server. Is the backend running?');
    } else {
      throw new Error(error.message || 'Failed to download module');
    }
  }
};

/**
 * List all generated modules
 * @returns {Promise<Array>} List of modules
 */
export const listModules = async () => {
  try {
    const response = await api.get('/list-modules');
    return response.data.modules || [];
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.message || 'Failed to list modules');
    } else if (error.request) {
      throw new Error('No response from server. Is the backend running?');
    } else {
      throw new Error(error.message || 'Failed to list modules');
    }
  }
};

/**
 * Health check endpoint
 * @returns {Promise<Object>} Health status
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    throw new Error('Backend is not available');
  }
};

export default api;


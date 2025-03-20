import axios from 'axios'

const API_URL = 'http://localhost:5000/api/music-boxes' // Backend API URL

const apiService = {
  async getMusicBoxes() {
    try {
      const response = await axios.get(API_URL)
      return response.data
    } catch (error) {
      if (!error.response) {
        console.warn('Backend not available. Using mock data.')
        return [
          { id: 1, name: 'Box 1', image: '/image/nootnoot.png', color: '#ff0000', isOn: false },
          { id: 2, name: 'Box 2', image: '/image/nootnoot.png', color: '#00ff00', isOn: false },
          { id: 3, name: 'Box 3', image: '/image/nootnoot.png', color: '#0000ff', isOn: false },
        ]
      } else {
        console.error('An error occurred:', error.message)
        throw error
      }
    }
  },

  async togglePower(id, isOn) {
    try {
      const response = await axios.put(`${API_URL}/${id}/toggle`, { isOn })
      return response.data
    } catch (error) {
      console.warn(`Failed to toggle power for Box ${id}:`, error.message)
      throw error
    }
  },

  async updateColor(id, color) {
    try {
      const response = await axios.put(`${API_URL}/${id}/color`, { color })
      return response.data
    } catch (error) {
      console.warn(`Failed to update color for Box ${id}:`, error.message)
      throw error
    }
  },

  async updateSound(id, sound) {
    try {
      const response = await axios.put(`${API_URL}/${id}/sound`, { sound });
      return response.data;
    } catch (error) {
      console.warn(`Failed to update sound for Box ${id}:`, error.message);
      throw error;
    }
  },
}

export default apiService

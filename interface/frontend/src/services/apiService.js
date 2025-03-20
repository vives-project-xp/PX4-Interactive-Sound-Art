import axios from 'axios';

const API_URL = 'http://localhost:4000/devices'; // Backend API URL

const apiService = {
  async getMusicBoxes() {
    try {
      const response = await axios.get(API_URL);
      return Object.entries(response.data).map(([boxId, device]) => ({
        id: boxId,
        name: `Box ${boxId}`,
        image: '/image/notenottransparent.png',
        color: device.color || '#ffffff',
        isOn: device.isOn || false,
        effect: device.effect || 'pulsating',
        sound: device.instrument || 'Piano',
        led: device.led || false
      }));
    } catch (error) {
      if (!error.response) {
        console.warn('Backend not available. Using mock data.');
        return [
          {
            id: 1,
            name: 'Box 1',
            image: '/image/piano.png',
            color: '#ff0000',
            isOn: false,
            effect: 'pulsating',
            sound: 'Piano',
            led: false
          },
          {
            id: 2,
            name: 'Box 2',
            image: '/image/guitar.png',
            color: '#00ff00',
            isOn: false,
            effect: 'firework',
            sound: 'Guitar',
            led: false
          },
          {
            id: 3,
            name: 'Box 3',
            image: '/image/violin.png',
            color: '#0000ff',
            isOn: false,
            effect: 'rainbow',
            sound: 'Violin',
            led: false
          }
        ];
      } else {
        console.error('An error occurred:', error.message);
        throw error;
      }
    }
  },

  async togglePower(id, isOn) {
    try {
      const response = await axios.post(`${API_URL}/${id}/command`, { isOn });
      return response.data;
    } catch (error) {
      console.warn(`Failed to toggle power for Box ${id}:`, error.message);
      throw error;
    }
  },

  async updateColor(id, color) {
    try {
      const response = await axios.post(`${API_URL}/${id}/command`, { color });
      return response.data;
    } catch (error) {
      console.warn(`Failed to update color for Box ${id}:`, error.message);
      throw error;
    }
  },

  async updateEffect(id, effect) {
    try {
      const response = await axios.post(`${API_URL}/${id}/command`, { effect });
      return response.data;
    } catch (error) {
      console.warn(`Failed to update effect for Box ${id}:`, error.message);
      throw error;
    }
  },

  

  async updateSound(id, sound) {
    try {
      const response = await axios.post(`${API_URL}/${id}/command`, { instrument: sound });
      return response.data;
    } catch (error) {
      console.warn(`Failed to update sound for Box ${id}:`, error.message);
      throw error;
    }
  }
};

export default apiService;

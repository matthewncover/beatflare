import React, { useEffect, useState, useCallback } from 'react';

// Types for our state and messages
type LED = {
  color: string;  // Hex color string (e.g., "#ff0000")
  index: number;
}

type ServerUpdate = {
  index: number;
  color: string;  // Hex color from server
}

const LEDStrip = () => {
    const [leds, setLeds] = useState<LED[]>(() => 
    Array.from({ length: 12 }, (_, index) => ({
        color: '#333333',
        index
    }))
  );
  
  const [ws, setWs] = useState<WebSocket | null>(null);

  const updateLEDs = useCallback((updates: ServerUpdate[]) => {
    setLeds(prevLeds => {
      const newLeds = [...prevLeds];
      updates.forEach(update => {
        const { index, color } = update;
        newLeds[index] = { ...newLeds[index], color };
      });
      return newLeds;
    });
  }, []);

  // Set up WebSocket connection
  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws');

    websocket.onopen = () => {
      console.log('Connected to WebSocket');
    };

    websocket.onmessage = (event) => {
        console.log('WebSocket received:', event.data);
        const data = JSON.parse(event.data);
        if (data.updates) {
            updateLEDs(data.updates);
        }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    setWs(websocket);

    return () => websocket.close();
  }, [updateLEDs]);

  return (
    <div className="p-8">
      <h2 className="text-xl mb-4">LED Strip Simulator</h2>
      
      {/* Connection status */}
      <div className="mb-4">
        <span className={`inline-block w-3 h-3 rounded-full mr-2 ${
          ws?.readyState === WebSocket.OPEN ? 'bg-green-500' : 'bg-red-500'
        }`}></span>
        {ws?.readyState === WebSocket.OPEN ? 'Connected' : 'Disconnected'}
      </div>

      {/* LED strip */}
      <div className="flex gap-2 p-4 bg-gray-800 rounded-lg">
        {leds.map((led) => (
          <div
            key={led.index}
            className="w-8 h-8 rounded-full"
            style={{
              backgroundColor: led.color,
              boxShadow: `0 0 10px ${led.color}`
            }}
          />
        ))}
      </div>
    </div>
  );
};

export default LEDStrip;

// import React from 'react';

// // Define a type for individual LED properties
// type LED = {
//   color: string;  // The current color of the LED
//   index: number;  // Position in the strip
// }

// const LEDStrip = () => {
//   // Create an array of 12 LEDs, initially all "off" (grey)
//   const leds: LED[] = Array.from({ length: 12 }, (_, index) => ({
//     color: '#333333',  // Dark grey represents an "off" state
//     index
//   }));

//   return (
//     // Container for the entire strip
//     <div className="p-8">
//       <h2 className="text-xl mb-4">LED Strip Simulator</h2>
      
//       {/* The strip itself - flex container to lay out LEDs horizontally */}
//       <div className="flex gap-2 p-4 bg-gray-800 rounded-lg">
//         {leds.map((led) => (
//           // Individual LED - using a div with rounded corners
//           <div
//             key={led.index}
//             className="w-8 h-8 rounded-full"
//             style={{
//               backgroundColor: led.color,
//               // Add a subtle glow effect
//               boxShadow: `0 0 10px ${led.color}`
//             }}
//           />
//         ))}
//       </div>
//     </div>
//   );
// };

// export default LEDStrip;
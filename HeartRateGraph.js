import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { LineChart } from 'react-native-chart-kit';

const screenWidth = Dimensions.get("window").width;

// Générer les labels temporels toutes les 30 secondes sur 15 min
const generateTimeLabels = () => {
  const labels = [];
  for (let i = 30; i >= 0; i--) {
    const seconds = i * 30;
    const min = Math.floor(seconds / 60);
    const sec = seconds % 60;
    labels.push(`${min}:${sec.toString().padStart(2, '0')}`);
  }
  return labels;
};

const timeLabels = generateTimeLabels();

// Fonction pour générer une valeur de rythme cardiaque aléatoire entre 70 et 80
const generateHeartRateValue = () => Math.floor(Math.random() * (80 - 70 + 1)) + 70;

export default function HeartRateGraph() {
  const [heartRateValues, setHeartRateValues] = useState(
    Array.from({ length: 31 }, generateHeartRateValue)
  );

  useEffect(() => {
    const interval = setInterval(() => {
      setHeartRateValues(prevValues => {
        const newValues = prevValues.slice(1); // Remove the oldest value
        newValues.push(generateHeartRateValue()); // Add a new value at the end
        return newValues;
      });
    }, 30000); // 30 seconds interval

    return () => clearInterval(interval); // Cleanup when component unmounts
  }, []);

  // Valeur minimale pour forcer l’échelle
  const minY = Math.max(0, Math.min(...heartRateValues) - 5);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Heart Rate (Last 15 Minutes)</Text>
      <LineChart
        data={{
          labels: timeLabels.map((label, index) =>
            index % 5 === 0 ? label : ''
          ),
          datasets: [
            {
              data: heartRateValues,
              strokeWidth: 2,
              color: () => `rgba(255, 99, 132, 1)`,
            },
            {
              data: [minY], // Valeur cachée pour fixer le Y min
              color: () => `rgba(0,0,0,0)`,
              withDots: false,
              withLines: false,
            },
          ],
        }}
        width={screenWidth - 20}
        height={240}
        yAxisSuffix=" bpm"
        yAxisInterval={1}
        chartConfig={{
          backgroundColor: '#ffffff',
          backgroundGradientFrom: '#f5f5f5',
          backgroundGradientTo: '#ffffff',
          decimalPlaces: 0,
          color: (opacity = 1) => `rgba(34, 128, 176, ${opacity})`,
          labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
          style: {
            borderRadius: 12,
          },
          propsForDots: {
            r: '3',
            strokeWidth: '1',
            stroke: '#1e90ff',
          },
        }}
        bezier
        style={{
          borderRadius: 12,
          marginVertical: 10,
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginTop: 20,
    padding: 10,
    backgroundColor: '#fff',
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
    elevation: 4,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 10,
    textAlign: 'center',
    color: '#333',
  },
});


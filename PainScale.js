import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { getDatabase, ref, set } from 'firebase/database';
import { database } from './firebase'; // adapte ce chemin selon ton projet

export default function PainScale({ patientId = 'patient_001' }) {
  const [selected, setSelected] = useState(null);

  const handleSelect = async (value) => {
    setSelected(value);

    // Création d’un timestamp sans date-fns
    const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);

    try {
      const db = getDatabase();
      const painRef = ref(db, `patients/${patientId}/painReports/${Date.now()}`);
      await set(painRef, {
        painLevel: value,
        timestamp: timestamp,
      });
      Alert.alert('Merci !', `Niveau de douleur enregistré : ${value}`);
    } catch (error) {
      Alert.alert('Erreur', "Impossible d'enregistrer le niveau de douleur.");
      console.error("Erreur Firebase:", error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Indiquez votre niveau de douleur :</Text>
      <View style={styles.scaleContainer}>
        {[...Array(10).keys()].map(i => {
          const value = i + 1;
          return (
            <TouchableOpacity
              key={value}
              style={[
                styles.circle,
                selected === value && styles.selectedCircle,
              ]}
              onPress={() => handleSelect(value)}
            >
              <Text style={styles.number}>{value}</Text>
            </TouchableOpacity>
          );
        })}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginTop: 20,
    alignItems: 'center',
  },
  label: {
    fontSize: 18,
    marginBottom: 15,
    color: '#333',
  },
  scaleContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
  },
  circle: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#ddd',
    justifyContent: 'center',
    alignItems: 'center',
    margin: 5,
  },
  selectedCircle: {
    backgroundColor: '#007bff',
  },
  number: {
    color: '#fff',
    fontWeight: 'bold',
  },
});

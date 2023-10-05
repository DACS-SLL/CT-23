package main

import "fmt"

// Encryptor interface
type Encryptor interface {
	Encrypt(data string) string
}

// Decryptor interface
type Decryptor interface {
	Decrypt(data string) string
}

// Factory of Encryption interface
type EncryptionFactory interface {
	CreateEncryptor() Encryptor
	CreateDecryptor() Decryptor
}

// DAC1 :) Encryptor
type DAC1Encryptor struct{}

func (e *DAC1Encryptor) Encrypt(data string) string {
	shift := 3 // go foward every character by 3 positions
	result := ""
	for _, r := range data {
		result += string(r + rune(shift))
	}
	return result
}

// DAC1 :0 Decryptor
type DAC1Decryptor struct{}

func (d *DAC1Decryptor) Decrypt(data string) string {
	shift := 3 // go back each character back by 3 positions
	result := ""
	for _, r := range data {
		result += string(r - rune(shift))
	}
	return result
}

// DAC2 x2 Encryptor
type DAC2Encryptor struct{}

func (e *DAC2Encryptor) Encrypt(data string) string {
	shift := 9 // go foward every character by 9 positions
	result := ""
	for _, r := range data {
		result += string(r + rune(shift))
	}
	return result
}

// DAC2 x2 :( Decryptor
type DAC2Decryptor struct{}

func (d *DAC2Decryptor) Decrypt(data string) string {
	shift := 9 // go back each character back by 9 positions
	result := ""
	for _, r := range data {
		result += string(r - rune(shift))
	}
	return result
}

// Concrete Factory for DAC1
type DAC1EncryptionFactory struct{}

func (f DAC1EncryptionFactory) CreateEncryptor() Encryptor {
	return &DAC1Encryptor{}
}

func (f DAC1EncryptionFactory) CreateDecryptor() Decryptor {
	return &DAC1Decryptor{}
}

// Concrete Factory for DAC2
type DAC2EncryptionFactory struct{}

func (f DAC2EncryptionFactory) CreateEncryptor() Encryptor {
	return &DAC2Encryptor{}
}

func (f DAC2EncryptionFactory) CreateDecryptor() Decryptor {
	return &DAC2Decryptor{}
}

// Main Code
func main() {
	// Using DAC1 Encryption
	dac1Factory := DAC1EncryptionFactory{}
	dac1Encryptor := dac1Factory.CreateEncryptor()
	dac1Decryptor := dac1Factory.CreateDecryptor()

	dataToEncrypt := "Hello, classmates! Today is a good day"
	encryptedData := dac1Encryptor.Encrypt(dataToEncrypt)
	decryptedData := dac1Decryptor.Decrypt(encryptedData)

	fmt.Println("Using DAC1 Encryption:")
	fmt.Println("Original Data:", dataToEncrypt)
	fmt.Println("Encrypted Data:", encryptedData)
	fmt.Println("Decrypted Data:", decryptedData)
	fmt.Println()

	// Using DAC2 Encryption
	dac2Factory := DAC2EncryptionFactory{}
	dac2Encryptor := dac2Factory.CreateEncryptor()
	dac2Decryptor := dac2Factory.CreateDecryptor()

	dataToEncrypt = "Hello, classmates! Today is a rainy day"
	encryptedData = dac2Encryptor.Encrypt(dataToEncrypt)
	decryptedData = dac2Decryptor.Decrypt(encryptedData)

	fmt.Println("Using DAC2 Encryption:")
	fmt.Println("Original Data:", dataToEncrypt)
	fmt.Println("Encrypted Data:", encryptedData)
	fmt.Println("Decrypted Data:", decryptedData)
}




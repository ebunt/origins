// The engine package defines the storage engine interface and default
// implementations. An appropriate storage engine is one that can be used
// as a key-value interface.
package engine

// Batch is group of key-value pairs that will be atomically set together.
type Batch map[[2]string][]byte

// Engine is an interface for defining storage engines.
type Engine interface {
	// Get takes a key and returns the associated bytes.
	Get(part, key string) ([]byte, error)

	// Set takes a key and bytes and writes it to the store.
	Set(part, key string, value []byte) error

	// SetMany takes a batch and writes it to the store.
	SetMany(Batch) error

	// Incr increments a stored number or sets it to one for new entries.
	Incr(part, key string) (uint64, error)
}

// Options is a general purpose map for accessing options for storage engines.
type Options map[string]interface{}

// Get returns the interface value associated with the key.
func (o Options) Get(k string) interface{} {
	return o[k]
}

// GetString returns a string value associated with the key.
// If the conversion fails, this will panic.
func (o Options) GetString(k string) string {
	if v, ok := o[k]; ok {
		return v.(string)
	}

	return ""
}

// GetInt returns an integer value associated with the key.
// If the conversion fails, this will panic.
func (o Options) GetInt(k string) int {
	if v, ok := o[k]; ok {
		return v.(int)
	}

	return 0
}

// GetBool returns a boolean value associated with the key.
// If the conversion fails, this will panic.
func (o Options) GetBool(k string) bool {
	if v, ok := o[k]; ok {
		return v.(bool)
	}

	return false
}

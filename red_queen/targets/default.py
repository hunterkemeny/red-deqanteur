from loader import _load_entry_point


def target_from_backend_str(backend_str):
    backend = _load_entry_point(f"qiskit.providers.fake_provider:{backend_str}")()

    return backend.target

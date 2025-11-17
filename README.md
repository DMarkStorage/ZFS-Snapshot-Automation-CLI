# ZFS Snapshot CLI Tool

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Python-based command-line tool for managing ZFS storage snapshots through REST API automation. Streamline snapshot operations, enable backup workflows, and generate audit-ready reports without manual console access.

## 🎯 Features

- **Snapshot Management**: Create, remove, and list snapshots programmatically
- **XCP Integration**: Built-in support for NetApp XCP migration snapshot verification
- **Automated Reporting**: Generates CSV and JSON exports for audit trails
- **API-Driven**: No SSH or console access required
- **Idempotent Operations**: Safe to re-run without side effects
- **Scriptable**: Easy integration with cron jobs and automation workflows

## 🚀 Use Cases

- Automated backup scheduling before maintenance windows
- Pre-migration snapshot verification for data migration tools
- Storage capacity reporting and stale snapshot identification
- Development environment snapshot management
- Compliance and audit trail generation

## 📋 Prerequisites

- Python 3.6 or higher
- Network access to ZFS storage appliance REST API (port 215)
- Valid authentication credentials for the storage appliance

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/DMarkStorage/ZFS-Snapshot-Automation-CLI.git
cd ZFS-Snapshot-Automation-CLI
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Update authentication credentials in `utils/parser.py`:
```python
headers = {
    "X-Auth-User": 'your_username',
    "X-Auth-Key": 'your_password'
}
```

## 📁 Project Structure

```
snapshotool/
├── tool.py              # Main entry point
├── utils/
│   ├── parser.py        # CLI argument parsing and headers
│   └── utils.py         # Core snapshot operations
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## 💻 Usage

### Create a Snapshot
```bash
python tool.py -s storage01.example.com -fs production_data -sp backup_20241117 --create
```

### List All Snapshots
```bash
python tool.py -s storage01.example.com -fs production_data --list
```

### Remove a Snapshot
```bash
python tool.py -s storage01.example.com -fs production_data -sp old_snapshot --remove
```

### Check for XCP-prefixed Snapshots
```bash
python tool.py -s storage01.example.com -fs migration_data --xcpfind
```

### Verify or Create Specific XCP Snapshot
```bash
python tool.py -s storage01.example.com -fs migration_data -sp xcp_baseline --xcp
```

### View Help
```bash
python tool.py --help
```

## 📊 Output Files

The tool automatically generates two files after each operation:

- **datafile.csv**: Comma-separated snapshot inventory (name, creation time, space used)
- **datafile.json**: Complete JSON response from the storage API

These files serve as audit trails and can be imported into spreadsheets or monitoring dashboards.

## 🔐 Security Considerations

⚠️ **Important**: The tool currently uses `verify=False` for SSL certificate validation to support lab environments with self-signed certificates. For production use:

1. Enable proper SSL verification by setting `verify=True` in all `requests` calls
2. Store credentials securely using environment variables or secret management tools
3. Implement proper certificate validation with your organization's CA bundle


## 🐛 Troubleshooting

**Connection Timeout**
- Verify network connectivity to the storage appliance on port 215
- Check firewall rules allow HTTPS traffic

**Authentication Failed**
- Verify credentials in `utils/parser.py`
- Ensure the user account has snapshot management permissions

**Filesystem Not Found**
- Verify the filesystem name matches exactly (case-sensitive)
- Use `--list` to see available filesystems first

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Roadmap

- [ ] Configuration file support for multiple appliances
- [ ] Retention policy management
- [ ] Bulk operations across multiple filesystems
- [ ] Email/Slack notifications
- [ ] Snapshot age reporting and cleanup recommendations
- [ ] Interactive mode for guided operations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Damini Marvin Mark**
- Website: [dmarkstorage.io](https://dmarkstorage.io)

## 🙏 Acknowledgments

- Built for storage engineers managing ZFS appliances
- Inspired by the need for scriptable snapshot management
- Designed to integrate with NetApp XCP migration workflows

## 📚 References

- [Python Requests Documentation](https://docs.python-requests.org/)
- [Docopt Documentation](http://docopt.org/)
- [Oracle ZFS REST API Guide](https://docs.oracle.com/cd/E51475_01/html/E52872/rest_api.html)

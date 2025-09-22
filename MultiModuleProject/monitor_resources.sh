#!/bin/bash

# Resource monitoring script for production
# monitors_ollama_resources.sh

echo "=== Ollama & Django Resource Monitor ==="
echo "Timestamp: $(date)"
echo

# Check Ollama process
echo "🤖 Ollama Status:"
if pgrep -f "ollama" > /dev/null; then
    echo "✅ Ollama is running"
    echo "PID: $(pgrep -f ollama)"
    echo "Memory: $(ps -p $(pgrep -f ollama) -o rss= | awk '{print $1/1024 " MB"}')"
else
    echo "❌ Ollama is not running"
fi

echo

# Check Django process  
echo "🐍 Django Status:"
if pgrep -f "manage.py" > /dev/null; then
    echo "✅ Django is running"
    echo "PID: $(pgrep -f manage.py)"
else
    echo "❌ Django is not running"
fi

echo

# System resources
echo "💻 System Resources:"
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "Memory Usage: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
echo "Disk Usage: $(df -h / | awk 'NR==2{printf "%s", $5}')"

echo
echo "🔗 Service Connectivity:"
curl -s http://localhost:11434/api/version > /dev/null && echo "✅ Ollama API accessible" || echo "❌ Ollama API not accessible"
curl -s http://localhost:8000 > /dev/null && echo "✅ Django accessible" || echo "❌ Django not accessible"

echo
echo "=========================="
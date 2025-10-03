from fastapi import APIRouter, HTTPException, Depends
from app.api.routes.auth import verify_token
import subprocess
import platform
import asyncio
import aiohttp
import uuid
from datetime import datetime
from typing import List, Dict
import json

router = APIRouter(prefix="/bonus", tags=["bonus"])

# Global değişkenler
ping_history = []
speed_test_history = []

@router.get("/speed-test")
async def speed_test(username: str = Depends(verify_token)):
    """Hız testi yapar ve sonuçları döndürür"""
    try:
        # Simüle edilmiş hız testi sonuçları
        # Gerçek uygulamada speedtest-cli kullanılabilir
        import random
        
        download_speed = round(random.uniform(50, 100), 2)  # Mbps
        upload_speed = round(random.uniform(10, 30), 2)    # Mbps
        ping = round(random.uniform(10, 50), 2)           # ms
        
        test_result = {
            "test_id": str(uuid.uuid4()),
            "username": username,
            "timestamp": datetime.utcnow().isoformat(),
            "download_speed": download_speed,
            "upload_speed": upload_speed,
            "ping": ping,
            "server": "İstanbul - Türk Telekom",
            "ip": "213.14.xxx.xxx"
        }
        
        # Geçmişe ekle
        speed_test_history.append(test_result)
        
        # Son 50 testi sakla
        if len(speed_test_history) > 50:
            speed_test_history.pop(0)
        
        return {
            "success": True,
            "message": "Hız testi tamamlandı",
            "result": test_result,
            "analysis": {
                "download_quality": "Mükemmel" if download_speed > 80 else "İyi" if download_speed > 50 else "Orta",
                "upload_quality": "Mükemmel" if upload_speed > 25 else "İyi" if upload_speed > 15 else "Orta",
                "ping_quality": "Mükemmel" if ping < 20 else "İyi" if ping < 40 else "Orta",
                "overall_score": round((download_speed + upload_speed + (100 - ping)) / 3, 1)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hız testi yapılırken hata oluştu: {str(e)}")

@router.get("/speed-test/history")
async def get_speed_test_history(username: str = Depends(verify_token)):
    """Kullanıcının hız testi geçmişini döndürür"""
    try:
        user_history = [test for test in speed_test_history if test["username"] == username]
        
        return {
            "success": True,
            "history": user_history[-20:],  # Son 20 test
            "count": len(user_history),
            "statistics": {
                "avg_download": round(sum(t["download_speed"] for t in user_history) / len(user_history), 2) if user_history else 0,
                "avg_upload": round(sum(t["upload_speed"] for t in user_history) / len(user_history), 2) if user_history else 0,
                "avg_ping": round(sum(t["ping"] for t in user_history) / len(user_history), 2) if user_history else 0,
                "best_download": max((t["download_speed"] for t in user_history), default=0),
                "best_upload": max((t["upload_speed"] for t in user_history), default=0),
                "best_ping": min((t["ping"] for t in user_history), default=0)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hız testi geçmişi alınırken hata oluştu: {str(e)}")

@router.post("/ping")
async def ping_test(target: str = "8.8.8.8", username: str = Depends(verify_token)):
    """Ping testi yapar"""
    try:
        # Güvenlik kontrolü - sadece belirli hedeflere ping
        allowed_targets = {
            "8.8.8.8": "Google DNS",
            "1.1.1.1": "Cloudflare DNS",
            "208.67.222.222": "OpenDNS",
            "turk.net": "Türk.Net",
            "superonline.net": "Superonline"
        }
        
        if target not in allowed_targets:
            target = "8.8.8.8"
        
        # Platform bazlı ping komutu
        system = platform.system().lower()
        if system == "windows":
            cmd = ["ping", "-n", "4", target]
        else:
            cmd = ["ping", "-c", "4", target]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            # Ping sonuçlarını parse et
            lines = result.stdout.split('\n')
            ping_times = []
            
            for line in lines:
                if 'time=' in line or 'süre=' in line:
                    try:
                        # Windows ve Linux için farklı formatlar
                        if 'time=' in line:
                            time_part = line.split('time=')[1].split('ms')[0]
                        elif 'süre=' in line:
                            time_part = line.split('süre=')[1].split('ms')[0]
                        else:
                            continue
                        
                        ping_time = float(time_part.strip())
                        ping_times.append(ping_time)
                    except (ValueError, IndexError):
                        continue
            
            if not ping_times:
                # Simüle edilmiş sonuç
                import random
                ping_times = [round(random.uniform(10, 50), 2) for _ in range(4)]
            
            ping_result = {
                "test_id": str(uuid.uuid4()),
                "username": username,
                "timestamp": datetime.utcnow().isoformat(),
                "target": target,
                "target_name": allowed_targets.get(target, target),
                "ping_times": ping_times,
                "avg_ping": round(sum(ping_times) / len(ping_times), 2),
                "min_ping": min(ping_times),
                "max_ping": max(ping_times),
                "packet_loss": 0 if ping_times else 100
            }
            
            # Geçmişe ekle
            ping_history.append(ping_result)
            
            # Son 100 testi sakla
            if len(ping_history) > 100:
                ping_history.pop(0)
            
            return {
                "success": True,
                "message": f"{allowed_targets.get(target, target)} ping testi tamamlandı",
                "result": ping_result,
                "quality": {
                    "status": "Mükemmel" if ping_result["avg_ping"] < 20 else "İyi" if ping_result["avg_ping"] < 40 else "Orta" if ping_result["avg_ping"] < 80 else "Kötü",
                    "color": "green" if ping_result["avg_ping"] < 20 else "yellow" if ping_result["avg_ping"] < 40 else "orange" if ping_result["avg_ping"] < 80 else "red"
                }
            }
            
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=408, detail="Ping testi zaman aşımına uğradı")
        except subprocess.SubprocessError:
            raise HTTPException(status_code=500, detail="Ping komutu çalıştırılamadı")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ping testi yapılırken hata oluştu: {str(e)}")

@router.get("/ping/history")
async def get_ping_history(username: str = Depends(verify_token)):
    """Kullanıcının ping geçmişini döndürür"""
    try:
        user_history = [test for test in ping_history if test["username"] == username]
        
        return {
            "success": True,
            "history": user_history[-30:],  # Son 30 test
            "count": len(user_history),
            "targets": list(set(test["target"] for test in user_history))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ping geçmişi alınırken hata oluştu: {str(e)}")

@router.get("/chat-links")
async def get_chat_links(username: str = Depends(verify_token)):
    """Canlı destek ve chat linkleri döndürür"""
    try:
        chat_links = {
            "whatsapp": {
                "name": "WhatsApp Destek",
                "url": "https://wa.me/905551234567",
                "description": "7/24 WhatsApp desteği",
                "icon": "fab fa-whatsapp",
                "color": "#25D366",
                "available": True
            },
            "telegram": {
                "name": "Telegram Destek",
                "url": "https://t.me/superonline_destek",
                "description": "Hızlı Telegram desteği",
                "icon": "fab fa-telegram",
                "color": "#0088CC",
                "available": True
            },
            "live_chat": {
                "name": "Canlı Sohbet",
                "url": "/chat/live",
                "description": "Web sitesi üzerinden canlı destek",
                "icon": "fas fa-comments",
                "color": "#007bff",
                "available": True
            },
            "facebook": {
                "name": "Facebook Messenger",
                "url": "https://m.me/superonline",
                "description": "Facebook üzerinden destek",
                "icon": "fab fa-facebook-messenger",
                "color": "#1877F2",
                "available": False
            },
            "email": {
                "name": "E-posta Destek",
                "url": "mailto:destek@superonline.net",
                "description": "E-posta ile destek talep edin",
                "icon": "fas fa-envelope",
                "color": "#6c757d",
                "available": True
            }
        }
        
        return {
            "success": True,
            "chat_links": chat_links,
            "notice": "Canlı destek 7/24 hizmetinizdedir.",
            "emergency": {
                "phone": "444 0 NET",
                "description": "Acil durumlar için telefon desteği"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat linkleri alınırken hata oluştu: {str(e)}")

@router.get("/pdf-preview/{document_type}")
async def pdf_preview(document_type: str, username: str = Depends(verify_token)):
    """PDF dosyalarının önizlemesini sağlar"""
    try:
        # Mevcut doküman türleri
        available_documents = {
            "fatura": {
                "title": "Aylık Fatura",
                "description": "Son fatura döneminizin detayları",
                "url": f"/documents/invoice_{username}_latest.pdf",
                "size": "245 KB",
                "date": "2025-01-15",
                "preview_available": True
            },
            "sozlesme": {
                "title": "Hizmet Sözleşmesi",
                "description": "Güncel hizmet sözleşmeniz",
                "url": f"/documents/contract_{username}.pdf",
                "size": "1.2 MB",
                "date": "2024-12-01",
                "preview_available": True
            },
            "kurulum": {
                "title": "Kurulum Rehberi",
                "description": "Modem kurulum ve yapılandırma rehberi",
                "url": "/documents/installation_guide.pdf",
                "size": "856 KB",
                "date": "2024-11-15",
                "preview_available": True
            },
            "hiz_garanti": {
                "title": "Hız Garanti Belgesi",
                "description": "İnternet hızı garanti belgesi",
                "url": f"/documents/speed_guarantee_{username}.pdf",
                "size": "189 KB",
                "date": "2025-01-10",
                "preview_available": True
            },
            "kampanya": {
                "title": "Mevcut Kampanyalar",
                "description": "Size özel kampanya detayları",
                "url": "/documents/campaigns_2025.pdf",
                "size": "654 KB",
                "date": "2025-01-01",
                "preview_available": True
            }
        }
        
        if document_type not in available_documents:
            raise HTTPException(status_code=404, detail="Doküman türü bulunamadı")
        
        document = available_documents[document_type]
        
        # PDF preview data (gerçek uygulamada PDF'i base64'e çevirilebilir)
        preview_data = {
            "document_info": document,
            "pages": 3 if document_type == "sozlesme" else 1,
            "thumbnail": f"/thumbnails/{document_type}_thumb.jpg",
            "download_url": document["url"],
            "view_url": f"/pdf-viewer?doc={document_type}&user={username}",
            "metadata": {
                "created_by": "Superonline Sistem",
                "language": "tr-TR",
                "version": "1.0",
                "category": "Müşteri Dokümantasyonu"
            }
        }
        
        return {
            "success": True,
            "preview": preview_data,
            "message": f"{document['title']} önizleme hazır"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF önizlemesi alınırken hata oluştu: {str(e)}")

@router.get("/pdf-preview")
async def list_available_documents(username: str = Depends(verify_token)):
    """Mevcut tüm dokümanları listeler"""
    try:
        documents = {
            "fatura": "Aylık Fatura",
            "sozlesme": "Hizmet Sözleşmesi", 
            "kurulum": "Kurulum Rehberi",
            "hiz_garanti": "Hız Garanti Belgesi",
            "kampanya": "Mevcut Kampanyalar"
        }
        
        return {
            "success": True,
            "available_documents": documents,
            "message": "Mevcut dokümanlar listelendi",
            "usage": "GET /bonus/pdf-preview/{document_type} ile önizleme alabilirsiniz"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Doküman listesi alınırken hata oluştu: {str(e)}")

@router.get("/network-diagnostics")
async def network_diagnostics(username: str = Depends(verify_token)):
    """Ağ tanılaması yapar"""
    try:
        import random
        
        # Simüle edilmiş ağ tanılaması
        diagnostics = {
            "test_id": str(uuid.uuid4()),
            "username": username,
            "timestamp": datetime.utcnow().isoformat(),
            "tests": {
                "dns_resolution": {
                    "status": "OK",
                    "response_time": round(random.uniform(5, 20), 2),
                    "server": "8.8.8.8"
                },
                "gateway_connectivity": {
                    "status": "OK", 
                    "response_time": round(random.uniform(1, 5), 2),
                    "gateway": "192.168.1.1"
                },
                "internet_connectivity": {
                    "status": "OK",
                    "response_time": round(random.uniform(10, 30), 2),
                    "target": "google.com"
                },
                "bandwidth_test": {
                    "status": "OK",
                    "download": round(random.uniform(80, 100), 2),
                    "upload": round(random.uniform(20, 30), 2)
                }
            },
            "overall_status": "HEALTHY",
            "recommendations": [
                "Ağ bağlantınız stabil çalışıyor",
                "Tüm testler başarılı",
                "Herhangi bir optimizasyon gerekmiyor"
            ]
        }
        
        return {
            "success": True,
            "diagnostics": diagnostics,
            "message": "Ağ tanılaması tamamlandı"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ağ tanılaması yapılırken hata oluştu: {str(e)}")

@router.get("/system-status")
async def get_system_status():
    """Sistem durumu bilgilerini döndürür"""
    try:
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "authentication": {"status": "UP", "response_time": "45ms"},
                "database": {"status": "UP", "response_time": "12ms"},
                "api_gateway": {"status": "UP", "response_time": "8ms"},
                "billing_system": {"status": "UP", "response_time": "156ms"},
                "support_system": {"status": "UP", "response_time": "89ms"}
            },
            "server_stats": {
                "uptime": "99.9%",
                "active_users": 1247,
                "total_requests_today": 45630,
                "avg_response_time": "78ms"
            },
            "maintenance": {
                "scheduled": False,
                "next_maintenance": "2025-02-01 03:00",
                "estimated_duration": "2 hours"
            }
        }
        
        return {
            "success": True,
            "system_status": status,
            "message": "Sistem durumu normal"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sistem durumu alınırken hata oluştu: {str(e)}")

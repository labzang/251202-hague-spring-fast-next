'use client';

import { useState, useRef, DragEvent } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface UploadedFile {
    id: string;
    name: string;
    size: number;
    type: string;
    url: string;
    uploadedAt: Date;
    file?: File; // 원본 File 객체 저장
}

export default function PortfolioPage() {
    const [files, setFiles] = useState<UploadedFile[]>([]);
    const [isDragOver, setIsDragOver] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragOver(true);
    };

    const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragOver(false);
    };

    const handleDrop = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragOver(false);

        const droppedFiles = Array.from(e.dataTransfer.files);

        // 파일 정보를 alert로 표시
        if (droppedFiles.length > 0) {
            // 파일 크기 포맷팅 함수 (로컬)
            const formatSize = (bytes: number) => {
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
            };

            let fileInfo = `📁 드롭된 파일 정보\n\n`;
            fileInfo += `총 파일 개수: ${droppedFiles.length}개\n\n`;

            droppedFiles.forEach((file, index) => {
                const fileSize = formatSize(file.size);
                const fileType = file.type || '알 수 없음';
                const lastModified = new Date(file.lastModified).toLocaleString('ko-KR');

                fileInfo += `[파일 ${index + 1}]\n`;
                fileInfo += `이름: ${file.name}\n`;
                fileInfo += `크기: ${fileSize}\n`;
                fileInfo += `타입: ${fileType}\n`;
                fileInfo += `수정일: ${lastModified}\n`;
                if (index < droppedFiles.length - 1) {
                    fileInfo += `\n`;
                }
            });

            alert(fileInfo);
        }

        processFiles(droppedFiles);
    };

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = Array.from(e.target.files || []);
        processFiles(selectedFiles);
    };

    const processFiles = (fileList: File[]) => {
        fileList.forEach(file => {
            // 파일 크기 제한 (10MB)
            if (file.size > 10 * 1024 * 1024) {
                alert(`파일 "${file.name}"이 너무 큽니다. 10MB 이하의 파일만 업로드 가능합니다.`);
                return;
            }

            // 지원하는 파일 형식 확인
            const supportedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'application/pdf', 'text/plain'];
            if (!supportedTypes.includes(file.type)) {
                alert(`파일 "${file.name}"은 지원하지 않는 형식입니다.`);
                return;
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                const newFile: UploadedFile = {
                    id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
                    name: file.name,
                    size: file.size,
                    type: file.type,
                    url: e.target?.result as string,
                    uploadedAt: new Date(),
                    file: file // 원본 File 객체 저장
                };

                setFiles(prev => [...prev, newFile]);
            };

            reader.readAsDataURL(file);
        });
    };

    const removeFile = (id: string) => {
        setFiles(prev => prev.filter(file => file.id !== id));
    };

    const formatFileSize = (bytes: number) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const getFileIcon = (type: string) => {
        if (type.startsWith('image/')) return '🖼️';
        if (type === 'application/pdf') return '📄';
        if (type.startsWith('text/')) return '📝';
        return '📁';
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">
                        포트폴리오 업로드
                    </h1>
                    <p className="text-lg text-gray-600">
                        드래그 앤 드롭으로 파일을 업로드하거나 클릭하여 파일을 선택하세요
                    </p>
                </div>

                {/* Upload Area */}
                <Card className="mb-8">
                    <div
                        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300 ${isDragOver
                            ? 'border-blue-500 bg-blue-50'
                            : 'border-gray-300 hover:border-gray-400'
                            }`}
                        onDragOver={handleDragOver}
                        onDragLeave={handleDragLeave}
                        onDrop={handleDrop}
                    >
                        <input
                            ref={fileInputRef}
                            type="file"
                            multiple
                            accept="image/*,.pdf,.txt"
                            onChange={handleFileSelect}
                            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        />

                        <div className="space-y-4">
                            <div className="text-6xl">📁</div>
                            <div>
                                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                    파일을 여기에 드래그하세요
                                </h3>
                                <p className="text-gray-600 mb-4">
                                    또는 클릭하여 파일을 선택하세요
                                </p>
                                <Button
                                    onClick={() => fileInputRef.current?.click()}
                                    className="bg-blue-600 hover:bg-blue-700"
                                >
                                    파일 선택
                                </Button>
                            </div>
                            <div className="text-sm text-gray-500">
                                지원 형식: JPG, PNG, GIF, WebP, PDF, TXT (최대 10MB)
                            </div>
                        </div>
                    </div>
                </Card>

                {/* Uploaded Files Grid */}
                {files.length > 0 && (
                    <div className="mb-8">
                        <h2 className="text-2xl font-bold text-gray-900 mb-4">
                            업로드된 파일 ({files.length}개)
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {files.map((file) => (
                                <Card key={file.id} className="p-4 hover:shadow-lg transition-shadow">
                                    <div className="flex items-start justify-between mb-3">
                                        <div className="flex items-center space-x-2">
                                            <span className="text-2xl">{getFileIcon(file.type)}</span>
                                            <div className="flex-1 min-w-0">
                                                <h3 className="font-medium text-gray-900 truncate">
                                                    {file.name}
                                                </h3>
                                                <p className="text-sm text-gray-500">
                                                    {formatFileSize(file.size)}
                                                </p>
                                            </div>
                                        </div>
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={() => removeFile(file.id)}
                                            className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                        >
                                            ✕
                                        </Button>
                                    </div>

                                    {/* File Preview */}
                                    {file.type.startsWith('image/') && (
                                        <div className="mb-3">
                                            <img
                                                src={file.url}
                                                alt={file.name}
                                                className="w-full h-32 object-cover rounded-md"
                                            />
                                        </div>
                                    )}

                                    <div className="flex justify-between items-center text-xs text-gray-500">
                                        <span>
                                            {file.uploadedAt.toLocaleDateString('ko-KR')} {file.uploadedAt.toLocaleTimeString('ko-KR')}
                                        </span>
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={() => {
                                                const link = document.createElement('a');
                                                link.href = file.url;
                                                link.download = file.name;
                                                link.click();
                                            }}
                                        >
                                            다운로드
                                        </Button>
                                    </div>
                                </Card>
                            ))}
                        </div>
                    </div>
                )}

                {/* Actions */}
                <div className="flex justify-center space-x-4">
                    <Button
                        variant="outline"
                        onClick={() => setFiles([])}
                        disabled={files.length === 0}
                    >
                        모든 파일 삭제
                    </Button>
                    <Button
                        onClick={async () => {
                            if (files.length === 0) {
                                alert('업로드할 파일이 없습니다.');
                                return;
                            }

                            setIsSaving(true);
                            const results: any[] = [];
                            const errors: string[] = [];

                            try {
                                console.log('[DEBUG] 파일 업로드 시작:', files.length, '개 파일');

                                // FastAPI 서버 URL
                                const API_URL = 'http://localhost:8000/api/upload';

                                // 각 파일을 개별적으로 업로드
                                for (const fileData of files) {
                                    if (!fileData.file) {
                                        errors.push(`${fileData.name}: 원본 파일을 찾을 수 없습니다.`);
                                        continue;
                                    }

                                    try {
                                        // FormData 생성
                                        const formData = new FormData();
                                        formData.append('file', fileData.file);

                                        console.log(`[DEBUG] 파일 업로드 중: ${fileData.name}`);

                                        // FastAPI로 파일 업로드
                                        const response = await fetch(API_URL, {
                                            method: 'POST',
                                            body: formData,
                                        });

                                        console.log(`[DEBUG] API 응답 상태: ${response.status} ${response.statusText}`);

                                        if (!response.ok) {
                                            const errorData = await response.json().catch(() => ({ detail: '알 수 없는 오류' }));
                                            throw new Error(errorData.detail || `HTTP ${response.status}`);
                                        }

                                        const data = await response.json();
                                        console.log('[DEBUG] API 응답 데이터:', data);

                                        results.push({
                                            filename: fileData.name,
                                            ...data
                                        });

                                    } catch (error: any) {
                                        console.error(`[ERROR] 파일 업로드 오류 (${fileData.name}):`, error);
                                        errors.push(`${fileData.name}: ${error.message || '알 수 없는 오류'}`);
                                    }
                                }

                                // 결과 표시
                                if (results.length > 0) {
                                    const successCount = results.length;
                                    const faceDetectionResults = results.filter(r => r.face_detection?.success);

                                    let message = `✅ ${successCount}개의 파일이 성공적으로 업로드되었습니다!\n\n`;

                                    if (faceDetectionResults.length > 0) {
                                        message += `얼굴 디텍션 결과:\n`;
                                        faceDetectionResults.forEach(r => {
                                            message += `- ${r.original_filename}: ${r.face_detection.face_count}개 얼굴 감지\n`;
                                        });
                                        message += `\n`;
                                    }

                                    message += `저장 경로: cv.lagzang.com/app/data/yolo/`;

                                    if (errors.length > 0) {
                                        message += `\n\n⚠️ 실패한 파일 (${errors.length}개):\n${errors.join('\n')}`;
                                    }

                                    alert(message);

                                    // 성공적으로 업로드된 후 파일 목록 초기화 (선택사항)
                                    // setFiles([]);
                                } else {
                                    alert(`❌ 모든 파일 업로드 실패:\n${errors.join('\n')}`);
                                }

                            } catch (error: any) {
                                console.error('[ERROR] 파일 업로드 오류:', error);
                                alert(`❌ 파일 업로드 중 오류가 발생했습니다: ${error.message || '알 수 없는 오류'}`);
                            } finally {
                                setIsSaving(false);
                            }
                        }}
                        disabled={files.length === 0 || isSaving}
                        className="bg-green-600 hover:bg-green-700 disabled:opacity-50"
                    >
                        {isSaving ? '업로드 중...' : `포트폴리오에 추가 (${files.length})`}
                    </Button>
                </div>

                {/* Back to Home */}
                <div className="text-center mt-8">
                    <Button
                        variant="outline"
                        onClick={() => window.history.back()}
                    >
                        ← 이전 페이지로
                    </Button>
                </div>
            </div>
        </div>
    );
}

import { NextRequest, NextResponse } from 'next/server';
import { writeFile, mkdir, unlink } from 'fs/promises';
import { join } from 'path';
import { existsSync } from 'fs';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  try {
    console.log('[API] 포트폴리오 파일 저장 요청 받음');
    const body = await request.json();
    const { files } = body;

    console.log('[API] 받은 파일 개수:', files?.length || 0);

    if (!files || !Array.isArray(files) || files.length === 0) {
      console.error('[API] 파일이 없음');
      return NextResponse.json(
        { error: '파일이 없습니다.' },
        { status: 400 }
      );
    }

    // 프로젝트 루트 경로
    const projectRoot = process.cwd();
    
    // 임시 파일 저장 경로
    const tempDir = join(projectRoot, '.temp', 'portfolio');
    if (!existsSync(tempDir)) {
      await mkdir(tempDir, { recursive: true });
    }

    const tempFiles: Array<{ name: string; path: string }> = [];
    const savedFiles: string[] = [];

    try {
      // 각 파일을 임시 폴더에 저장
      console.log(`[API] 임시 파일 저장 시작 (${files.length}개)`);
      for (const file of files) {
        const { name, url } = file;
        console.log(`[API] 파일 처리 중: ${name}`);

        // base64 데이터에서 실제 데이터 추출
        const base64Data = url.split(',')[1] || url;
        const buffer = Buffer.from(base64Data, 'base64');
        console.log(`[API] 파일 크기: ${buffer.length} bytes`);

        // 임시 파일 경로
        const tempFilePath = join(tempDir, name);
        await writeFile(tempFilePath, buffer);
        console.log(`[API] 임시 파일 저장 완료: ${tempFilePath}`);

        tempFiles.push({ name, path: tempFilePath });
        savedFiles.push(name);
      }
      console.log(`[API] 모든 임시 파일 저장 완료`);

      // Python 스크립트 경로
      const pythonScriptPath = join(
        projectRoot,
        '..',
        'cv.lagzang.com',
        'app',
        'yolo',
        'main.py'
      );

      // Python 스크립트 경로 확인
      console.log(`[API] Python 스크립트 경로 확인: ${pythonScriptPath}`);
      if (!existsSync(pythonScriptPath)) {
        console.error(`[API] Python 스크립트를 찾을 수 없음: ${pythonScriptPath}`);
        throw new Error(`Python 스크립트를 찾을 수 없습니다: ${pythonScriptPath}`);
      }
      console.log(`[API] Python 스크립트 경로 확인 완료`);

      // 파일 존재 확인
      for (const tempFile of tempFiles) {
        if (!existsSync(tempFile.path)) {
          throw new Error(`임시 파일이 생성되지 않았습니다: ${tempFile.path}`);
        }
        console.log(`[API] 임시 파일 존재 확인: ${tempFile.path}`);
      }

      // 파일 정보를 JSON 파일로 저장
      const jsonFilePath = join(tempDir, 'files.json');
      const jsonData = JSON.stringify(tempFiles, null, 2);
      await writeFile(jsonFilePath, jsonData, 'utf-8');
      console.log(`[API] JSON 파일 생성 완료: ${jsonFilePath}`);
      console.log(`[API] JSON 데이터:`, jsonData);
      
      // JSON 파일 존재 확인
      if (!existsSync(jsonFilePath)) {
        throw new Error(`JSON 파일이 생성되지 않았습니다: ${jsonFilePath}`);
      }

      // Python 명령어 확인
      const isWindows = process.platform === 'win32';
      
      // 가상환경 경로 확인 (프로젝트 루트 기준)
      const possiblePythonPaths = [
        // 가상환경 경로들 (프로젝트 루트 기준)
        join(projectRoot, '..', 'yolo11', isWindows ? 'Scripts' : 'bin', isWindows ? 'python.exe' : 'python'),
        join(projectRoot, '..', 'venv', isWindows ? 'Scripts' : 'bin', isWindows ? 'python.exe' : 'python'),
        join(projectRoot, '..', '.venv', isWindows ? 'Scripts' : 'bin', isWindows ? 'python.exe' : 'python'),
        // 시스템 Python
        isWindows ? 'python' : 'python3',
      ];

      // 사용 가능한 Python 경로 찾기
      let pythonCmd = isWindows ? 'python' : 'python3';
      for (const pythonPath of possiblePythonPaths) {
        if (typeof pythonPath === 'string' && pythonPath.includes('python')) {
          // 경로가 파일 경로인 경우
          if (pythonPath.includes('/') || pythonPath.includes('\\')) {
            if (existsSync(pythonPath)) {
              pythonCmd = pythonPath;
              console.log(`[INFO] 가상환경 Python 사용: ${pythonCmd}`);
              break;
            }
          }
        }
      }

      // Python 스크립트 실행 (JSON 파일 경로 전달)
      // Windows에서는 경로에 공백이 있을 수 있으므로 따옴표 처리
      const command = `"${pythonCmd}" "${pythonScriptPath}" --portfolio "${jsonFilePath}"`;
      
      console.log(`[API] Python 스크립트 실행 시작`);
      console.log(`[API] Python 명령어: ${pythonCmd}`);
      console.log(`[API] 스크립트 경로: ${pythonScriptPath}`);
      console.log(`[API] JSON 파일 경로: ${jsonFilePath}`);
      console.log(`[API] 전체 명령어: ${command}`);
      
      try {
        const { stdout, stderr } = await execAsync(command, {
          cwd: projectRoot,
          maxBuffer: 10 * 1024 * 1024, // 10MB
          shell: isWindows ? 'cmd.exe' : '/bin/bash',
        });

        console.log(`[API] Python 스크립트 실행 완료`);
        if (stderr) {
          console.log('[API] Python 스크립트 stderr:', stderr);
        }
        if (stdout) {
          console.log('[API] Python 스크립트 stdout:', stdout);
        }

        // yolo 폴더 경로
        const yoloDataPath = join(
          projectRoot,
          '..',
          'cv.lagzang.com',
          'app',
          'data',
          'yolo'
        );

        // Python 스크립트가 성공했으므로 임시 파일은 이미 이동됨 (삭제 불필요)
        // tempFiles는 Python 스크립트에서 이동되었으므로 finally 블록에서 삭제 시도하지 않음
        const movedFiles = [...tempFiles];
        tempFiles.length = 0; // finally 블록에서 삭제하지 않도록 비움

        return NextResponse.json({
          success: true,
          message: `${savedFiles.length}개의 파일이 성공적으로 yolo 폴더로 이동되었습니다.`,
          files: savedFiles,
          path: yoloDataPath,
        });
      } catch (execError: any) {
        console.error('[API] Python 스크립트 실행 오류 발생');
        console.error('[API] 에러 메시지:', execError.message);
        console.error('[API] 에러 코드:', execError.code);
        console.error('[API] 에러 전체:', JSON.stringify(execError, null, 2));
        
        // Python 스크립트 실행 실패 시 직접 저장 시도
        console.log('[API] Fallback: 직접 파일 이동 시도');
        const yoloDataPath = join(
          projectRoot,
          '..',
          'cv.lagzang.com',
          'app',
          'data',
          'yolo'
        );

        if (!existsSync(yoloDataPath)) {
          await mkdir(yoloDataPath, { recursive: true });
        }

        // 임시 파일을 yolo 폴더로 이동 (Python 스크립트 실패 시 직접 처리)
        for (const tempFile of tempFiles) {
          const destPath = join(yoloDataPath, tempFile.name);
          const fs = await import('fs/promises');
          // 파일 이동 (rename 사용)
          await fs.rename(tempFile.path, destPath);
        }
        
        // 이동 완료된 파일은 삭제 목록에서 제외
        tempFiles.length = 0;

        return NextResponse.json({
          success: true,
          message: `${savedFiles.length}개의 파일이 성공적으로 저장되었습니다. (Python 스크립트 실패, 직접 저장)`,
          files: savedFiles,
          path: yoloDataPath,
        });
      }
    } finally {
      // 임시 파일 삭제
      for (const tempFile of tempFiles) {
        try {
          await unlink(tempFile.path);
        } catch (error) {
          console.error(`임시 파일 삭제 실패: ${tempFile.path}`, error);
        }
      }
      
      // JSON 파일 삭제
      try {
        const jsonFilePath = join(tempDir, 'files.json');
        if (existsSync(jsonFilePath)) {
          await unlink(jsonFilePath);
        }
      } catch (error) {
        console.error('JSON 파일 삭제 실패:', error);
      }
    }
  } catch (error: any) {
    console.error('파일 저장 오류:', error);
    return NextResponse.json(
      { error: '파일 저장 중 오류가 발생했습니다.', details: error.message },
      { status: 500 }
    );
  }
}

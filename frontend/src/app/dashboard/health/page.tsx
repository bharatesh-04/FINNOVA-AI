'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function HealthPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-primary-text">Financial Health</h1>

      <Card>
        <CardHeader>
          <CardTitle>Your Financial Health Score</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-secondary-text">Comprehensive analysis of your financial well-being.</p>
        </CardContent>
      </Card>
    </div>
  );
}
